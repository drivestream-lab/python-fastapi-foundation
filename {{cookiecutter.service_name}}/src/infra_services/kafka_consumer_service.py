"""Kafka consumer service stub for {{cookiecutter.service_name}}."""

from injector import inject
from src.infra_services.base_infra_service import BaseInfraService
from src.logging import get_logger

logger = get_logger()


class KafkaConsumerService(BaseInfraService):
    """aiokafka consumer loop. Implement in W0 (topic routing in feature waves)."""

    @inject
    def __init__(self) -> None:
        self._running = False

    async def initialize(self) -> None:
        logger.info("KafkaConsumerService.initialize — implement in W0")
        self._running = True

    async def close(self) -> None:
        self._running = False

    async def health_check(self) -> bool:
        return self._running
