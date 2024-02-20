class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_409 = 409


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = "0000",
        msg: str = "",
        ex: Exception = Exception(),
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.ex = ex
        super().__init__(ex)


class NotAuthorization(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'1'.zfill(4)}",
            msg=f"Not Authorization",
            ex=ex,
        )


class ExpireJwtToken(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'2'.zfill(4)}",
            msg=f"Expire JWT Token",
            ex=ex,
        )


class NotFoundUserEx(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"해당 유저를 찾을 수 없습니다.",
            code=f"{StatusCode.HTTP_401}{'3'.zfill(4)}",
            ex=ex,
        )


class BadPassword(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"Bad password",
            code=f"{StatusCode.HTTP_401}{'4'.zfill(4)}",
            ex=ex,
        )


class DuplicateUserEx(APIException):
    def __init__(self, ex: Exception = Exception(), user_id=""):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'5'.zfill(4)}",
            msg=f"ID가 {user_id}인 유저가 존재합니다.",
            ex=ex,
        )


class InvalidJwtToken(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            code=f"{StatusCode.HTTP_401}{'6'.zfill(4)}",
            msg=f"Invalid JWT Token",
            ex=ex,
        )


class InternalSqlEx(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            code=f"{StatusCode.HTTP_500}{'1'.zfill(4)}",
            msg=f"SQL error",
            ex=ex,
        )


class InternalQuerryEx(APIException):
    def __init__(self, ex: Exception = Exception()):
        super().__init__(
            code=f"{StatusCode.HTTP_500}{'2'.zfill(4)}",
            msg=f"Query error",
            ex=ex,
        )
