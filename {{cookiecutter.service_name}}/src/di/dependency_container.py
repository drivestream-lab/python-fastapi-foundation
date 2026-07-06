"""Dependency injection container for {{cookiecutter.service_name}}."""

from typing import Optional, Type, TypeVar

from injector import Injector

from src.logging import get_logger
{%- if cookiecutter.has_telemetry == "yes" %}
from src.infra_services.telemetry_service import TelemetryService
{%- endif %}
{%- if cookiecutter.has_postgres == "yes" %}
from src.infra_services.postgres_service import PostgresService
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
from src.infra_services.redis_service import RedisService
{%- endif %}
{%- if cookiecutter.has_kafka == "yes" %}
from src.infra_services.kafka_consumer_service import KafkaConsumerService
{%- endif %}
{%- if cookiecutter.has_s3 == "yes" %}
from src.infra_services.s3_service import S3Service
{%- endif %}
{%- if cookiecutter.has_cratedb == "yes" %}
from src.infra_services.cratedb_service import CrateDBService
{%- endif %}
{%- if cookiecutter.has_emqx == "yes" %}
from src.infra_services.emqx_publish_service import EmqxPublishService
{%- endif %}

T = TypeVar("T")
_injector: Optional[Injector] = None
logger = get_logger()

# Keep in sync with bindings in src/di/modules/infra_module.py (lifecycle services only).
_INFRA_SERVICE_TYPES: tuple[type, ...] = (
{%- if cookiecutter.has_telemetry == "yes" %}
    TelemetryService,
{%- endif %}
{%- if cookiecutter.has_postgres == "yes" %}
    PostgresService,
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
    RedisService,
{%- endif %}
{%- if cookiecutter.has_kafka == "yes" %}
    KafkaConsumerService,
{%- endif %}
{%- if cookiecutter.has_s3 == "yes" %}
    S3Service,
{%- endif %}
{%- if cookiecutter.has_cratedb == "yes" %}
    CrateDBService,
{%- endif %}
{%- if cookiecutter.has_emqx == "yes" %}
    EmqxPublishService,
{%- endif %}
)

# Keep in sync with bindings in src/di/modules/business_services_module.py.
_BUSINESS_SERVICE_TYPES: tuple[type, ...] = (
    # Add business services as feature waves deliver them.
)


def configure_container() -> Injector:
    from src.di.modules.business_services_module import BusinessServicesModule
    from src.di.modules.infra_module import InfraModule

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
