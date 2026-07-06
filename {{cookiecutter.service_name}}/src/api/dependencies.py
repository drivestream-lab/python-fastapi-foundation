"""FastAPI dependency providers for {{cookiecutter.service_name}}.

Infra getters live here. ``provide_service`` is imported inside each getter to avoid
circular imports with ``dependency_container``.
"""

{% if cookiecutter.has_postgres == "yes" %}
from src.infra_services.postgres_service import PostgresService
{%- endif %}{% if cookiecutter.has_redis == "yes" %}
from src.infra_services.redis_service import RedisService
{%- endif %}


{% if cookiecutter.has_postgres == "yes" %}
def get_postgres_service() -> PostgresService:
    """Resolve PostgresService from the injector container."""
    from src.di.dependency_container import provide_service

    return provide_service(PostgresService)

{% endif %}
{% if cookiecutter.has_redis == "yes" %}
def get_redis_service() -> RedisService:
    """Resolve RedisService from the injector container."""
    from src.di.dependency_container import provide_service

    return provide_service(RedisService)

{% endif %}
