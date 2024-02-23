from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Database:
    def __init__(self, conf) -> None:
        if conf.get("TEST_MODE", False) is True:
            self._engine = create_async_engine(
                url=f'postgresql+asyncpg://{str(conf.get("DB_USER", ""))}:{str(conf.get("DB_PASSWORD", ""))}@{str(conf.get("DB_HOST", ""))}:{str(conf.get("DB_PORT", ""))}/test_db',
                pool_pre_ping=True,
                echo=True,
            )
        else:
            self._engine = create_async_engine(
                url=f'postgresql+asyncpg://{str(conf.get("DB_USER", ""))}:{str(conf.get("DB_PASSWORD", ""))}@{str(conf.get("DB_HOST", ""))}:{str(conf.get("DB_PORT", ""))}/{str(conf.get("DB_NAME", ""))}',
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

    @property
    def engine(self):
        return self._engine
