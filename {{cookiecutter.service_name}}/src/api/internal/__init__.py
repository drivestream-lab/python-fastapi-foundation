"""Internal router for {{cookiecutter.service_name}} (service-to-service, not public)."""

from fastapi import APIRouter

internal_router = APIRouter(prefix="/internal", tags=["Internal"])
