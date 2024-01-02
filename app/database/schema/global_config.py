from sqlalchemy import Column, Integer, String

from app.database.base import BaseMixin

from .base import Base


class GlobalConfig(Base, BaseMixin):
    __tablename__ = "global_config"
    global_config_no = Column(Integer, primary_key=True, index=True)
    value = Column(String(255))
    default_value = Column(String(255), nullable=False)
    parameter = Column(String(255), nullable=False)
    is_enable = Column(Integer, nullable=False)
