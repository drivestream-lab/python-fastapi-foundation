"""Health check router for {{cookiecutter.service_name}}."""

from fastapi import APIRouter, Depends, Query

{% if cookiecutter.has_postgres == "yes" %}
from src.api.dependencies import get_postgres_service
from src.infra_services.postgres_service import PostgresService
{% endif %}
{% if cookiecutter.has_redis == "yes" %}
from src.api.dependencies import get_redis_service
from src.infra_services.redis_service import RedisService
{% endif %}
from src.logging import get_logger
from src.models.health_models import (
    HealthDetailedResponse,
    HealthSimpleResponse,
    HealthStatusType,
    ServiceHealthDetailModel,
)

logger = get_logger()
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthSimpleResponse | HealthDetailedResponse)
async def health_check(
    detailed: bool = Query(default=False, description="Return detailed dependency health"),
{%- if cookiecutter.has_postgres == "yes" %}
    postgres_service: PostgresService = Depends(get_postgres_service),
{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
    redis_service: RedisService = Depends(get_redis_service),
{%- endif %}
) -> HealthSimpleResponse | HealthDetailedResponse:
    """GET /health — simple liveness by default; ?detailed=true checks infra."""
    if not detailed:
        return HealthSimpleResponse()

    all_healthy = True
    services: dict[str, ServiceHealthDetailModel] = {}

{%- if cookiecutter.has_postgres == "yes" %}
    postgres_healthy = False
    try:
        postgres_healthy = await postgres_service.health_check()
    except Exception as e:
        logger.error("Error checking PostgreSQL health", error=str(e))
    services["postgres"] = ServiceHealthDetailModel(
        status=HealthStatusType.UP if postgres_healthy else HealthStatusType.DOWN,
        details={"healthy": postgres_healthy},
    )
    all_healthy = all_healthy and postgres_healthy

{%- endif %}
{%- if cookiecutter.has_redis == "yes" %}
    redis_healthy = False
    try:
        redis_healthy = await redis_service.health_check()
    except Exception as e:
        logger.error("Error checking Redis health", error=str(e))
    services["redis"] = ServiceHealthDetailModel(
        status=HealthStatusType.UP if redis_healthy else HealthStatusType.DOWN,
        details={"healthy": redis_healthy},
    )
    all_healthy = all_healthy and redis_healthy

{%- endif %}
    agg = HealthStatusType.UP if all_healthy else HealthStatusType.DOWN
    return HealthDetailedResponse(status=agg, services=services)
