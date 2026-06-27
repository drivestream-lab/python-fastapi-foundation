"""FastAPI dependency providers for {{cookiecutter.service_name}}."""

from src.di.dependency_container import provide_service

{% if cookiecutter.has_postgres == "yes" %}
from src.infra_services.postgres_service import PostgresService

def get_postgres_service() -> PostgresService:
    return provide_service(PostgresService)
{% endif %}
{% if cookiecutter.has_redis == "yes" %}
from src.infra_services.redis_service import RedisService

def get_redis_service() -> RedisService:
    return provide_service(RedisService)
{% endif %}
