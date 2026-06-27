"""Kavach client settings for {{cookiecutter.service_name}}."""

from typing import ClassVar
from pydantic import Field
from src.configs.base_settings import BaseSettings


class KavachSettings(BaseSettings):
    PREFIX: ClassVar[str] = "KAVACH"

    base_url: str = Field(default="http://localhost:8005")
    timeout_seconds: int = Field(default=10)
    internal_api_key: str = Field(default="")
