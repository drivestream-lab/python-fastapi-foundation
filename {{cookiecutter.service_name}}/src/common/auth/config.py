"""JWT auth config for {{cookiecutter.service_name}}."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AuthConfig:
    issuer: str
    audience: str
    public_paths: List[str] = field(default_factory=lambda: ["/health"])
    algorithm: str = "RS256"
    public_key_path: Optional[str] = None
    secret_key: Optional[str] = None
