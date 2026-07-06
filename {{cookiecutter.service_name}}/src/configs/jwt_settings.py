"""JWT settings for {{cookiecutter.service_name}}."""

from typing import ClassVar

from pydantic import Field
from src.configs.base_settings import BaseSettings


class JWTSettings(BaseSettings):
    PREFIX: ClassVar[str] = "JWT"

    issuer: str = Field(default="identity-service")
    audience: str = Field(default="{{cookiecutter.service_name}}")
    algorithm: str = Field(default="RS256")
    public_key_path: str = Field(default="keys/public.pem")
