import json
from typing import AsyncIterator

import fakeredis.aioredis
from common.config import get_config
from dependency_injector.wiring import Provide, inject
from redis import asyncio as aioredis


async def init_redis_pool(conf: get_config) -> AsyncIterator[aioredis.Redis]:
    if conf["TEST_MODE"]:
        session = await fakeredis.aioredis.FakeRedis()
    else:
        session = aioredis.from_url(
            f"redis://{str(conf.get('REDIS_HOST', ''))}",
            port=int(str(conf.get("REDIS_PORT", 6379))),
            password=str(conf.get("REDIS_PASSWORD")),
        )
    yield session
    await session.close()


@inject
async def get_user_cahce(login_id: str, conf: get_config, redis=Provide["redis"]) -> str | None:
    """
    유저정보 캐시로 관리
    """
    try:
        if redis is None:
            raise ValueError("Redis 인스턴스가 초기화되지 않았습니다.")
        cahce_user = await redis.get(f"cahce_user_info_{login_id}")
        if cahce_user is None:
            await redis.set(
                name=f"cahce_user_info_{login_id}",
                value=str(json.dumps(cahce_user)),
                ex=conf["redis_expire_time"],
            )
            cahce_user = await redis.get(f"cahce_user_info_{login_id}")
        if isinstance(cahce_user, bytes):
            cahce_user = cahce_user.decode()
            return cahce_user
        else:
            return None
    except Exception as e:
        print(e)
        return None
