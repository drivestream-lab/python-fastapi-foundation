"""Infra DI module for {{cookiecutter.service_name}} — bindings driven by scaffold flags."""

from injector import Binder, Module, singleton

from src.logging import get_logger

logger = get_logger()


class InfraModule(Module):
    """Register infrastructure services enabled at scaffold time."""

    def configure(self, binder: Binder) -> None:
        logger.info("Configuring infrastructure services module")
{%- if cookiecutter.has_telemetry == "yes" %}
        from src.infra_services.telemetry_service import TelemetryService

        binder.bind(TelemetryService, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_postgres == "yes" %}
        from src.infra_services.postgres_service import PostgresService

        binder.bind(PostgresService, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
        from src.infra_services.redis_service import RedisService

        binder.bind(RedisService, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_kafka == "yes" %}
        from src.infra_services.kafka_consumer_service import KafkaConsumerService

        binder.bind(KafkaConsumerService, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_s3 == "yes" %}
        from src.infra_services.s3_service import S3Service

        binder.bind(S3Service, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_cratedb == "yes" %}
        from src.infra_services.cratedb_service import CrateDBService

        binder.bind(CrateDBService, scope=singleton)
{%- endif %}
{%- if cookiecutter.has_emqx == "yes" %}
        from src.infra_services.emqx_publish_service import EmqxPublishService

        binder.bind(EmqxPublishService, scope=singleton)
{%- endif %}
{%- if cookiecutter.parichay_client == "yes" %}
        from src.infra_services.parichay_client import ParichayClient

        binder.bind(ParichayClient, scope=singleton)
{%- endif %}
{%- if cookiecutter.abhilekh_client == "yes" %}
        from src.infra_services.abhilekh_client import AbhilekhClient

        binder.bind(AbhilekhClient, scope=singleton)
{%- endif %}
{%- if cookiecutter.kavach_client == "yes" %}
        from src.infra_services.kavach_client import KavachClient

        binder.bind(KavachClient, scope=singleton)
{%- endif %}
        logger.debug("Infrastructure services module configured")
