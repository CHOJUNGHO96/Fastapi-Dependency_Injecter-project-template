import re
import time
from typing import Optional

import sqlalchemy.exc
from dependency_injector import containers
from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.config import get_config
from app.database.redis_config import RedisConfig
from app.errors.exceptions import (APIException, InternalSqlEx,
                                   NotAuthorization, NotFoundUserEx)
from app.models.user import ModelTokenData
from app.util.date_utils import D
from app.util.logger import LogAdapter


async def base_control_middlewares(request: Request, call_next):
    """
    베이스 미들웨어
    이 함수는 모든 HTTP 요청에 대해 호출됩니다.
    여기에는 요청 로깅, 토큰 검증, 에러 처리 등이 포함됩니다.

    :param request: `들어오는 HTTP 요청을 나타냅니다.\n
    Request 객체는 요청 헤더, 경로, 쿼리 파라미터 등 요청과 관련된 다양한 정보를 담고 있습니다.`

    :param call_next: `다음 미들웨어 또는 실제 요청을 처리하는 경로 작업을 호출하는 함수입니다.\n
    이 함수를 호출하면 요청이 다음 단계로 전달되며, 결과로 나오는 응답(Response 객체)을 받을 수 있습니다.`
    """
    container: containers = request.app.container
    config: get_config = container.config()
    logger: LogAdapter = container.logging()
    redis: RedisConfig = container.redis()

    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None

    headers = request.headers

    # 프록시를 사용하여 x-forwarded-for 헤더가 있으면 그 값을, 없으면 클라이언트의 IP 주소를 사용합니다.
    if "x-forwarded-for" in request.headers:
        ip = request.headers["x-forwarded-for"]
    elif request.client is not None and request.client.host is not None:
        ip = request.client.host
    else:
        ip = "unknown"
    request.state.ip = ip.split(",")[0] if "," in ip else ip

    # 토큰검증없이 접속가능한 url 처리 작업
    url = request.url.path
    if await url_pattern_check(url, "^(/docs|/redoc|/api/v1/auth)") or url in [
        "/",
        "/openapi.json",
    ]:
        response = await call_next(request)
        if url != "/":
            await logger.api_logger(request=request, response=response)
        return response

    # 토큰검증후 HTTP 요청처리
    try:
        # 로그인 인증후 들어오는 요청은 토큰검사를 해야함
        if "authorization" in headers.keys():
            if "Bearer" in str(headers.get("authorization")):
                token = str(headers.get("authorization")).replace("Bearer ", "")
            else:
                token = str(headers.get("authorization"))

            # 들어온 토큰 유효성 검사
            await get_current_user(conf=config, redis=redis, token=token)
        else:
            raise NotAuthorization()
        return await call_next(request)
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await logger.api_logger(request=request, error=error)
        return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    print(error)
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = InternalSqlEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error)
    return error


async def get_current_user(conf: get_config(), redis: RedisConfig, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, conf["JWT_SECRET_KEY"], algorithms=conf["JWT_ALGORITHM"])
        # user_id 추출
        payload_sub = payload.get("sub")
        payload_user_id = payload.get("user_id")
        user_id: Optional[str] = payload_sub if payload_sub is not None else payload_user_id
        if user_id is None:
            raise credentials_exception
        token_data = ModelTokenData(user_id=user_id, token=token)
    except JWTError:
        raise credentials_exception
    if token_data.user_id is not None:
        # 레디스에서 유저정보 가져오기
        user_info = await redis.get_user_cahce(user_id=user_id)
        if not user_info:
            raise NotFoundUserEx()
        return True
    else:
        raise NotAuthorization()
