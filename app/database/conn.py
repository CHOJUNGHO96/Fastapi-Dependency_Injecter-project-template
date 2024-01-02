from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, conf) -> None:
        self._engine = create_async_engine(
            str(conf.get("DB_URL", "")),
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )

        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    @asynccontextmanager
    async def session(
        self,
    ) -> AsyncIterator[AbstractAsyncContextManager[AsyncSession]]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
