"""Config loader — resolves all settings objects for {{cookiecutter.service_name}}."""

from src.configs.app_settings import AppSettings
{%- if cookiecutter.has_postgres == "yes" %}
from src.configs.postgres_settings import PostgresSettings
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
from src.configs.redis_settings import RedisSettings
{%- endif %}
{%- if cookiecutter.has_kafka == "yes" %}
from src.configs.kafka_settings import KafkaSettings
{%- endif %}
{%- if cookiecutter.has_s3 == "yes" %}
from src.configs.s3_settings import S3Settings
{%- endif %}
{%- if cookiecutter.has_cratedb == "yes" %}
from src.configs.cratedb_settings import CrateDBSettings
{%- endif %}
{%- if cookiecutter.auth_mode == "jwt" %}
from src.configs.jwt_settings import JWTSettings
{%- endif %}
{%- if cookiecutter.has_telemetry == "yes" %}
from src.configs.telemetry_settings import TelemetrySettings
{%- endif %}
{%- if cookiecutter.parichay_client == "yes" %}
from src.configs.parichay_settings import ParichaySettings
{%- endif %}
{%- if cookiecutter.abhilekh_client == "yes" %}
from src.configs.abhilekh_settings import AbhilekhSettings
{%- endif %}
{%- if cookiecutter.kavach_client == "yes" %}
from src.configs.kavach_settings import KavachSettings
{%- endif %}


def load_all_settings():
    """Eagerly validate all settings at startup. Fails fast on misconfiguration."""
    AppSettings.get_instance()
    {%- if cookiecutter.has_postgres == "yes" %}
    PostgresSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.has_redis == "yes" %}
    RedisSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.has_kafka == "yes" %}
    KafkaSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.has_s3 == "yes" %}
    S3Settings.get_instance()
    {%- endif %}
    {%- if cookiecutter.has_cratedb == "yes" %}
    CrateDBSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.auth_mode == "jwt" %}
    JWTSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.has_telemetry == "yes" %}
    TelemetrySettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.parichay_client == "yes" %}
    ParichaySettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.abhilekh_client == "yes" %}
    AbhilekhSettings.get_instance()
    {%- endif %}
    {%- if cookiecutter.kavach_client == "yes" %}
    KavachSettings.get_instance()
    {%- endif %}
