from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: int
    msg: str
    code: str
    list: list
