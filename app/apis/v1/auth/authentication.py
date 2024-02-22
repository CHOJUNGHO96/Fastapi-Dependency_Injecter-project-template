from datetime import datetime, timedelta

from app.errors import exceptions as ex
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authentication:
    @classmethod
    def create_jwt_token(cls, data: dict, conf: dict, token_type: str) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=conf.get(f"JWT_{token_type}_TOKEN_EXPIRE_MINUTES"))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf[f"JWT_{token_type}_SECRET_KEY"], algorithm=conf["JWT_ALGORITHM"])
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
