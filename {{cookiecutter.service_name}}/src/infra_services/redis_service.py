"""Redis service for {{cookiecutter.service_name}}."""

from injector import inject
from src.infra_services.base_infra_service import BaseInfraService
from src.logging import get_logger

logger = get_logger()


class RedisService(BaseInfraService):
    """Async Redis client. Implement fully in W0."""

    @inject
    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        logger.info("RedisService.initialize — implement in W0")
        self._initialized = True

    async def close(self) -> None:
        self._initialized = False

    async def health_check(self) -> bool:
        return self._initialized
