"""FastAPI dependency providers for {{cookiecutter.service_name}}.

Infra getters live here. ``provide_service`` is imported inside each getter to avoid
circular imports with ``dependency_container`` (parichay pattern).
"""

{% if cookiecutter.has_postgres == "yes" %}
from src.infra_services.postgres_service import PostgresService
{%- endif %}{% if cookiecutter.has_redis == "yes" %}
from src.infra_services.redis_service import RedisService
{%- endif %}{% if cookiecutter.parichay_client == "yes" %}
from src.infra_services.parichay_client import ParichayClient
{%- endif %}{% if cookiecutter.abhilekh_client == "yes" %}
from src.infra_services.abhilekh_client import AbhilekhClient
{%- endif %}{% if cookiecutter.kavach_client == "yes" %}
from src.infra_services.kavach_client import KavachClient
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
{% if cookiecutter.parichay_client == "yes" %}
def get_parichay_client() -> ParichayClient:
    """Resolve ParichayClient from the injector container."""
    from src.di.dependency_container import provide_service

    return provide_service(ParichayClient)

{% endif %}
{% if cookiecutter.abhilekh_client == "yes" %}
def get_abhilekh_client() -> AbhilekhClient:
    """Resolve AbhilekhClient from the injector container."""
    from src.di.dependency_container import provide_service

    return provide_service(AbhilekhClient)

{% endif %}
{% if cookiecutter.kavach_client == "yes" %}
def get_kavach_client() -> KavachClient:
    """Resolve KavachClient from the injector container."""
    from src.di.dependency_container import provide_service

    return provide_service(KavachClient)

{% endif %}
