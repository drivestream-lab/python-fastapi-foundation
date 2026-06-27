"""Redis connection pool for {{cookiecutter.service_name}}."""

from redis.asyncio import Redis, ConnectionPool
from src.configs.redis_settings import RedisSettings
from src.logging import get_logger

logger = get_logger()
_pool: ConnectionPool | None = None


def init_pool() -> Redis:
    global _pool
    settings = RedisSettings.get_instance()
    _pool = ConnectionPool(**settings.connection_params)
    logger.info("Redis pool initialised")
    return Redis(connection_pool=_pool)


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.aclose()
        _pool = None
