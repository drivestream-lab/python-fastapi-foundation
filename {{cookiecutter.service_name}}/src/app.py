"""FastAPI application setup for {{cookiecutter.service_name|title}}."""

import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.health.health_router import router as health_router
from src.api.v1 import api_router
from src.configs.app_settings import AppSettings
from src.exceptions.app_exceptions import BaseAppException
from src.logging import get_logger, setup_logging, LoggingContext
from src.utils.correlation_id import CorrelationIdMiddleware
from src.di.dependency_container import (
    configure_container,
    initialize_all_services,
    close_all_services,
)


{% if cookiecutter.has_internal_api == "yes" %}
from src.api.internal import internal_router
{% endif %}
{% if cookiecutter.has_telemetry == "yes" %}
from src.infra_services.telemetry_service import TelemetryService
from src.di.dependency_container import provide_service
{% endif %}
{% if cookiecutter.auth_mode == "jwt" %}
from src.common.auth import AuthConfig, AuthMiddleware
from src.configs.jwt_settings import JWTSettings
{% endif %}

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_id = str(uuid.uuid4())
    with LoggingContext(startup_id):
        logger.info("Starting {{cookiecutter.service_name}} application")
        container = configure_container()
        app.state.container = container
        try:
            await initialize_all_services()
{% if cookiecutter.has_telemetry == "yes" %}
            provide_service(TelemetryService).instrument_app(app)
{% endif %}
            logger.info("All services initialized successfully")
        except Exception:
            logger.exception("Service initialization failed")
            raise
        logger.complete()
    yield
    with LoggingContext(startup_id):
        logger.info("Shutting down {{cookiecutter.service_name}} application")
        try:
            await close_all_services()
        except Exception as e:
            logger.error("Error during shutdown", error=str(e))


def create_app() -> FastAPI:
    settings = AppSettings.get_instance()
    setup_logging(settings)

    app = FastAPI(
        title="{{cookiecutter.service_name|title}} API",
        description="My Service for DriveStream",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
{% if cookiecutter.auth_mode == "jwt" %}
    jwt_settings = JWTSettings.get_instance()
    auth_config = AuthConfig(
        issuer=jwt_settings.issuer,
        audience=jwt_settings.audience,
        public_key_path=jwt_settings.public_key_path,
        public_paths=[
            "/health",
{% if cookiecutter.has_internal_api == "yes" %}
            "/internal",
{% endif %}
        ],
        algorithm="RS256",
    )
    app.add_middleware(AuthMiddleware, config=auth_config)
{% endif %}

    app.add_middleware(CorrelationIdMiddleware)

    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
        cid = getattr(request.state, "correlation_id", "")
        logger.error(
            "Application error",
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
            correlation_id=cid,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error": {"code": exc.code, "message": exc.message, "details": exc.details},
                "metadata": {"timestamp": str(time.time()), "correlation_id": cid},
            },
        )

    app.include_router(health_router)
{% if cookiecutter.has_internal_api == "yes" %}
    app.include_router(internal_router)
{% endif %}
    app.include_router(api_router, prefix="/api/v1")

    logger.info("FastAPI application configured")
    return app
