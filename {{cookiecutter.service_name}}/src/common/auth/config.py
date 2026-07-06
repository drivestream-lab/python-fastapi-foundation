"""JWT auth config for {{cookiecutter.service_name}}."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AuthConfig:
    """RS256 JWT verification config (platform identity issuer)."""

    issuer: str
    audience: str
    public_key_path: str
    public_paths: List[str] = field(default_factory=lambda: ["/health"])
    algorithm: str = "RS256"
