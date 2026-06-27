"""EMQX publish settings for {{cookiecutter.service_name}}."""

from typing import ClassVar
from pydantic import Field
from src.configs.base_settings import BaseSettings


class EmqxSettings(BaseSettings):
    PREFIX: ClassVar[str] = "EMQX"

    http_api_url: str = Field(default="http://localhost:18083/api/v5")
    api_key: str = Field(default="")
    api_secret: str = Field(default="")
    timeout_seconds: int = Field(default=5)
