from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.errors import exceptions as ex

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication:
    @classmethod
    def create_jwt_access_token(cls, data: dict, conf: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=conf.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf["JWT_SECRET_KEY"], algorithm=conf["JWT_ALGORITHM"])
        return encoded_jwt

    @classmethod
    def get_password_hash(cls, password):
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            raise ex.BadPassword()
