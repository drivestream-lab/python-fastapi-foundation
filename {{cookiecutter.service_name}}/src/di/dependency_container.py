"""Dependency injection container for {{cookiecutter.service_name}}."""

from typing import Optional, Type, TypeVar
from injector import Injector
from src.logging import get_logger

T = TypeVar("T")
_injector: Optional[Injector] = None
logger = get_logger()

# ── Register infra services here (keep in sync with InfraModule) ──────────────
# Add service types as you implement each wave.
_INFRA_SERVICE_TYPES: tuple[type, ...] = (
    # TelemetryService,   # uncomment after implementing W0
    # PostgresService,    # uncomment after implementing W0
    # RedisService,       # uncomment after implementing W0
    # KafkaConsumerService,  # uncomment after implementing W0
    # ParichayClient,     # uncomment after implementing W0
)

# ── Register business services here (keep in sync with BusinessServicesModule) ─
_BUSINESS_SERVICE_TYPES: tuple[type, ...] = (
    # Add as waves deliver them
)


def configure_container() -> Injector:
    from src.di.modules.infra_module import InfraModule
    from src.di.modules.business_services_module import BusinessServicesModule

    global _injector
    if _injector is None:
        logger.info("Configuring DI container")
        _injector = Injector([InfraModule(), BusinessServicesModule()])
        logger.info("DI container configured")
    return _injector


async def initialize_all_services() -> None:
    logger.info("Initializing all services")
    injector = get_container()
    for svc_type in _INFRA_SERVICE_TYPES:
        await injector.get(svc_type).initialize()
    for svc_type in _BUSINESS_SERVICE_TYPES:
        await injector.get(svc_type).initialize()
    logger.info("All services initialized")


async def close_all_services() -> None:
    logger.info("Closing all services")
    injector = get_container()
    for svc_type in reversed(_BUSINESS_SERVICE_TYPES):
        try:
            await injector.get(svc_type).close()
        except Exception as e:
            logger.warning("Error closing service", service=svc_type.__name__, error=str(e))
    for svc_type in reversed(_INFRA_SERVICE_TYPES):
        try:
            await injector.get(svc_type).close()
        except Exception as e:
            logger.warning("Error closing service", service=svc_type.__name__, error=str(e))


def get_container() -> Injector:
    global _injector
    if _injector is None:
        raise RuntimeError("Call configure_container() first")
    return _injector


def reset_container() -> None:
    global _injector
    _injector = None


def provide_service(cls: Type[T]) -> T:
    return get_container().get(cls)
