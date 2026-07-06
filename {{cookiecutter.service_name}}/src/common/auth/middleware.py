"""JWT verification middleware (RS256, platform identity issuer)."""

from typing import Callable, Optional
from uuid import UUID

from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.common.auth.config import AuthConfig
from src.models.auth_models import AuthContext

_OWNER_ROLES = frozenset({"owner", "tenant_owner"})


class AuthMiddleware(BaseHTTPMiddleware):
    """Validates Authorization Bearer JWT (RS256) and sets request.state.auth."""

    def __init__(self, app, config: AuthConfig) -> None:
        super().__init__(app)
        self._config = config
        if config.algorithm.upper() != "RS256":
            raise ValueError("Only RS256 JWT verification is supported")
        if not config.public_key_path:
            raise ValueError("JWT_PUBLIC_KEY_PATH is required for RS256 verification")
        with open(config.public_key_path) as key_file:
            self._verify_key_cached = key_file.read()

    def _is_public_path(self, path: str) -> bool:
        """Check if path is in public_paths (exact or prefix)."""
        for public_path in self._config.public_paths:
            if path == public_path or path.rstrip("/") == public_path.rstrip("/"):
                return True
            if public_path.endswith("/") and path.startswith(public_path):
                return True
            if not public_path.endswith("/") and path.startswith(public_path + "/"):
                return True
        return False

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate Bearer JWT; set request.state.auth or return 401."""
        path = request.scope.get("path") or request.url.path

        if self._is_public_path(path):
            setattr(request.state, "auth", None)
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Missing or invalid Authorization header",
                    },
                },
            )

        token = auth_header[7:].strip()
        if not token:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Missing Bearer token",
                    },
                },
            )

        try:
            payload = jwt.decode(
                token,
                self._verify_key_cached,
                algorithms=["RS256"],
                audience=self._config.audience,
                issuer=self._config.issuer,
            )
        except JWTError as exc:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Invalid or expired token",
                        "details": str(exc),
                    },
                },
            )

        sub = payload.get("sub")
        tenant_id_raw = payload.get("tenant_id")
        role = payload.get("role")
        if not sub:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {"code": "UNAUTHORIZED", "message": "Token missing sub"},
                },
            )

        try:
            user_id = UUID(sub)
        except (ValueError, TypeError):
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "error": {"code": "UNAUTHORIZED", "message": "Invalid sub in token"},
                },
            )

        tenant_id: Optional[UUID] = None
        if tenant_id_raw is not None:
            try:
                tenant_id = UUID(tenant_id_raw)
            except (ValueError, TypeError):
                pass

        owner_id: Optional[UUID] = None
        if (role or "").strip().lower() in _OWNER_ROLES:
            owner_id_raw = payload.get("owner_id") or sub
            try:
                owner_id = UUID(owner_id_raw)
            except (ValueError, TypeError):
                owner_id = user_id

        auth_context = AuthContext.model_validate(
            {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "role": role if role else "tenant_admin",
                "owner_id": owner_id,
            }
        )
        setattr(request.state, "auth", auth_context)
        return await call_next(request)
