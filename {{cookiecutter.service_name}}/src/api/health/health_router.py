"""Health check router for {{cookiecutter.service_name}}."""

from fastapi import APIRouter, Query
from src.logging import get_logger
from src.models.health_models import (
    HealthDetailedResponse, HealthSimpleResponse, HealthStatusType, ServiceHealthDetailModel,
)

{% if cookiecutter.has_postgres == "yes" %}
from fastapi import Depends
from src.infra_services.postgres_service import PostgresService
{% endif %}
{% if cookiecutter.has_redis == "yes" %}
from fastapi import Depends
from src.infra_services.redis_service import RedisService
{% endif %}

logger = get_logger()
router = APIRouter(tags=["Health"])


async def _check(name: str, fn) -> tuple[bool, dict]:
    try:
        ok = await fn()
        return ok, {"healthy": ok}
    except Exception as e:
        logger.error("Health check failed", service=name, error=str(e))
        return False, {"healthy": False}


@router.get("/health", response_model=HealthSimpleResponse | HealthDetailedResponse)
async def health_check(
    detailed: bool = Query(default=False, description="Return detailed dependency health"),
{%- if cookiecutter.has_postgres == "yes" %}
    postgres_service: PostgresService = Depends(lambda: None),  # inject via DI after W0
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
    redis_service: RedisService = Depends(lambda: None),        # inject via DI after W0
{%- endif %}
) -> HealthSimpleResponse | HealthDetailedResponse:
    """GET /health — simple liveness by default; ?detailed=true checks all infra."""
    if not detailed:
        return HealthSimpleResponse()

    services: dict[str, ServiceHealthDetailModel] = {}
    all_healthy = True

{%- if cookiecutter.has_postgres == "yes" %}
    ok, det = await _check("postgres", postgres_service.health_check) if postgres_service else (False, {"healthy": False})
    services["postgres"] = ServiceHealthDetailModel(
        status=HealthStatusType.UP if ok else HealthStatusType.DOWN, details=det)
    all_healthy = all_healthy and ok
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
    ok, det = await _check("redis", redis_service.health_check) if redis_service else (False, {"healthy": False})
    services["redis"] = ServiceHealthDetailModel(
        status=HealthStatusType.UP if ok else HealthStatusType.DOWN, details=det)
    all_healthy = all_healthy and ok
{%- endif %}

    return HealthDetailedResponse(
        status=HealthStatusType.UP if all_healthy else HealthStatusType.DOWN,
        services=services,
    )
