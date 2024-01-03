from dependency_injector import containers, providers
from fastapi.requests import Request

from app.apis.v1.auth.login.containers import Container as LoginContainer
from app.apis.v1.auth.registration.containers import Container as RegistrationContainer
from app.common.config import get_config
from app.database.conn import Database
from app.util.logger import LogAdapter
from app.util.token import Token
from app.database.redis_config import RedisConfig


class Container(containers.DeclarativeContainer):
    # config 의존성 주입
    config = providers.Configuration()
    config.from_dict(get_config().dict())

    # token 의존성 주입
    token = providers.Singleton(Token)

    # logging 의존성 주입
    logging = providers.Singleton(LogAdapter, request=Request, response=None, error=None)

    # db 의존성 주입
    db = providers.Singleton(Database, conf=config)

    # Redis 의존성 주입
    redis = providers.Singleton(RedisConfig, conf=config)

    # api 의존성 주입
    providers.Container(LoginContainer, db=db, config=config, token=token)
    providers.Container(RegistrationContainer, db=db, config=config, token=token)
