import json
from typing import Optional

from redis import Redis
from sqlalchemy import text

from app.database.conn import db
from app.util.init_template import QUERY_TEMPLATE
from app.util.jinja_sql import JINJA_SQL


class RedisConfig:
    """
    Redis 설정
    """

    host: Optional[str] = ""
    port: int = 0
    password: Optional[str] = None
    redis_expire_time: int = 900
    redis: Optional[Redis] = None

    def __init__(self, **conf: dict):
        self.host = str(conf.get("REDIS_HOST", ""))
        self.port = int(str(conf.get("REDIS_PORT", 6379)))
        self.password = str(conf.get("REDIS_PASSWORD"))
        self.redis_expire_time = int(str(conf.get("REDIS_EXPIRE_TIME", 900)))
        self.redis = Redis(host=self.host, port=self.port, password=self.password)

    def get_global_config(self) -> str:
        """
        전역설정값을 Redis에 저장
        """
        if self.redis is None:
            raise ValueError("Redis 인스턴스가 초기화되지 않았습니다.")
        global_config = self.redis.get("global_config")

        db_session = next(db.get_db())
        query = QUERY_TEMPLATE["global_config.yaml"]["전역환경값 조회"]
        _global_config_data = db_session.execute(text(query)).fetchall()
        global_config_data = json.dumps({data.parameter: data.value for data in _global_config_data})

        if global_config is None:
            self.redis.set(
                name="global_config",
                value=str(global_config_data),
                ex=self.redis_expire_time,
            )
            global_config = self.redis.get("global_config")

        if isinstance(global_config, bytes):
            global_config = global_config.decode()
            return global_config
        else:
            return ""

    def get_user_cahce(self, user_id: str) -> str:
        """
        유저정보를 Redis에 저장
        """
        if self.redis is None:
            raise ValueError("Redis 인스턴스가 초기화되지 않았습니다.")

        cahce_user = self.redis.get(f"cahce_user_info_{user_id}")

        db_session = next(db.get_db())
        query, bind_param = JINJA_SQL["named"].prepare_query(QUERY_TEMPLATE["login.yaml"]["유저조회"], {"user_id": user_id})
        _user_info = db_session.execute(text(query), bind_param).mappings().all()
        _user_info = [dict(row) for row in _user_info][0]
        del _user_info["user_password"]
        user_info = json.dumps(_user_info)

        if cahce_user is None:
            self.redis.set(
                name=f"cahce_user_info_{user_id}",
                value=str(user_info),
                ex=self.redis_expire_time,
            )
            cahce_user = self.redis.get(f"cahce_user_info_{user_id}")

        if isinstance(cahce_user, bytes):
            cahce_user = cahce_user.decode()
            return cahce_user
        else:
            return ""
