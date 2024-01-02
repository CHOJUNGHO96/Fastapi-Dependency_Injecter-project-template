from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.user import TokenData, UserBase, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, user_id: str):
    if user_id in db:
        user_dict = db[user_id]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, user_id: str, password: str):
    user = get_user(fake_db, user_id)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(user: UserBase, conf: dict, token: Annotated[str, Depends(oauth2_scheme)]):
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
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    if token_data.user_id is not None:
        user = get_user(user, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


class Token:
    @classmethod
    async def get_current_active_user(cls, current_user: Annotated[UserBase, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    @classmethod
    def create_access_token(cls, data: dict, conf: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=conf.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf["JWT_SECRET_KEY"], algorithm=conf["JWT_ALGORITHM"])
        return encoded_jwt
