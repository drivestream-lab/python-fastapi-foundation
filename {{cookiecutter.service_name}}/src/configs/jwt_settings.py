"""JWT settings for {{cookiecutter.service_name}} (Parichay-issued tokens)."""

from typing import ClassVar, Optional
from pydantic import Field
from src.configs.base_settings import BaseSettings


class JWTSettings(BaseSettings):
    PREFIX: ClassVar[str] = "JWT"

    issuer: str = Field(default="parichay")
    audience: str = Field(default="{{cookiecutter.service_name}}")
    algorithm: str = Field(default="RS256")
    public_key_path: Optional[str] = Field(default=None)
    secret_key: Optional[str] = Field(default=None)
