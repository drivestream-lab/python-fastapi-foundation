"""Correlation ID middleware for {{cookiecutter.service_name}}."""

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from src.logging import get_logger, set_correlation_id

logger = get_logger()
_HEADER_NAME = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Outermost request middleware: stamps one correlation ID per request."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        cid = request.headers.get(_HEADER_NAME, "").strip() or str(uuid.uuid4())
        request.state.correlation_id = cid
        set_correlation_id(cid)
        start = time.time()
        logger.debug(
            "Request started", correlation_id=cid, method=request.method, path=request.url.path
        )
        response = await call_next(request)
        logger.debug(
            "Request completed",
            correlation_id=cid,
            method=request.method,
            path=request.url.path,
            duration_seconds=round(time.time() - start, 3),
        )
        response.headers[_HEADER_NAME] = cid
        return response
