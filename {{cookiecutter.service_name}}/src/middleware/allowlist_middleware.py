"""Source-service allowlist middleware for {{cookiecutter.service_name}}."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.logging import get_logger

logger = get_logger()

# TODO W0: load from AllowlistSettings or env var ALLOWLIST_SOURCE_SERVICES
_ALLOWED_SERVICES: set[str] = set()


class AllowlistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/health"):
            return await call_next(request)
        source = request.headers.get("X-Source-Service", "").strip()
        if source not in _ALLOWED_SERVICES:
            logger.warning("Rejected request from unlisted source", source_service=source)
            return JSONResponse(status_code=403,
                                content={"status": "error",
                                         "error": {"code": "FORBIDDEN",
                                                    "message": f"Source service '{source}' not allowlisted"}})
        return await call_next(request)
