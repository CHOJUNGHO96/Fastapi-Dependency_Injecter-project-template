from sqlalchemy import Column, Integer, String

from app.database.base import BaseMixin

from .base import Base


class User(Base, BaseMixin):
    __tablename__ = "user_info"

    user_number = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False)
    user_password = Column(String(100), nullable=False)
    user_email = Column(String(100), nullable=False)
    user_name = Column(String(50), nullable=False)
    is_enable = Column(Integer, nullable=False)
