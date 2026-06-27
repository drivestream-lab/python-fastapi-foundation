"""Base infrastructure service for {{cookiecutter.service_name}}."""

import abc
from src.logging import get_logger

logger = get_logger()


class BaseInfraService(abc.ABC):
    """Abstract base for all infrastructure services.

    Subclasses must use @inject on __init__ and be registered in InfraModule
    via binder.bind(ServiceClass, scope=singleton).
    """

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Initialize the service and open external resources."""

    @abc.abstractmethod
    async def close(self) -> None:
        """Close the service and release resources."""

    @abc.abstractmethod
    async def health_check(self) -> bool:
        """Return True if the service is reachable and healthy."""
