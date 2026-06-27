"""PostgreSQL async engine + session factory for {{cookiecutter.service_name}}."""

from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.configs.postgres_settings import PostgresSettings
from src.logging import get_logger

logger = get_logger()
_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    settings = PostgresSettings.get_instance()
    engine = create_async_engine(settings.sqlalchemy_database_uri,
                                  **settings.sqlalchemy_engine_args)
    _session_factory = async_sessionmaker(engine, expire_on_commit=False)
    logger.info("Postgres engine initialised")
    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    if _session_factory is None:
        raise RuntimeError("Call init_engine() first")
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
