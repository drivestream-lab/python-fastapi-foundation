"""Base business service for {{cookiecutter.service_name}}."""

import abc
from src.logging import get_logger


class BaseBusinessService(abc.ABC):
    """Abstract base for all business services."""

    def __init__(self) -> None:
        self._initialized = False
        self.logger = get_logger()
        self.logger.info("Service created", service_class=self.__class__.__name__)

    async def initialize(self) -> None:
        self.logger.info("Service initializing", service_class=self.__class__.__name__)
        self._initialized = True

    async def close(self) -> None:
        self.logger.info("Service closing", service_class=self.__class__.__name__)
        self._initialized = False

    async def health_check(self) -> bool:
        return self._initialized
