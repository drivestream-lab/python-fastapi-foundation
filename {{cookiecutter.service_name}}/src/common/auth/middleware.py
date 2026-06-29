"""JWT auth middleware for {{cookiecutter.service_name}} (Parichay-issued tokens)."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.common.auth.config import AuthConfig
from src.logging import get_logger

logger = get_logger()


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: AuthConfig) -> None:
        super().__init__(app)
        self.config = config

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(p) for p in self.config.public_paths):
            return await call_next(request)
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        if not token:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {"code": "UNAUTHORIZED", "message": "Missing token"},
                },
            )
        # TODO W0: verify JWT with python-jose using self.config.public_key_path
        return await call_next(request)
