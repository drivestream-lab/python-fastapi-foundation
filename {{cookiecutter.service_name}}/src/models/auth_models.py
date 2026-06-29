"""Auth context models for JWT-protected routes."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

_OWNER_ROLES = frozenset({"owner", "tenant_owner"})


class AuthContext(BaseModel):
    """Authenticated request context set by JWT middleware."""

    model_config = ConfigDict(extra="forbid")

    user_id: UUID = Field(description="Authenticated user identifier")
    tenant_id: Optional[UUID] = Field(
        default=None,
        description="Tenant identifier for tenant-scoped users",
    )
    role: str = Field(description="Authenticated role code from JWT")
    owner_id: Optional[UUID] = Field(
        default=None,
        description="Set when role is owner or tenant_owner",
    )

    def is_owner_role(self) -> bool:
        """True when JWT role is owner or tenant_owner."""
        return self.role.strip().lower() in _OWNER_ROLES
