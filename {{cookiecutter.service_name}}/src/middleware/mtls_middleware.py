"""mTLS middleware for {{cookiecutter.service_name}}."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.logging import get_logger

logger = get_logger()


class MtlsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/health"):
            return await call_next(request)
        # TODO W0: verify client cert from request headers (nginx passes X-SSL-Client-Cert)
        return await call_next(request)
