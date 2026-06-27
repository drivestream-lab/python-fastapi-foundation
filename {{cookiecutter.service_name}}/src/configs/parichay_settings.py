"""Parichay client settings for {{cookiecutter.service_name}}."""

from typing import ClassVar
from pydantic import Field
from src.configs.base_settings import BaseSettings


class ParichaySettings(BaseSettings):
    PREFIX: ClassVar[str] = "PARICHAY"

    base_url: str = Field(default="http://localhost:8000")
    timeout_seconds: int = Field(default=10)
    internal_api_key: str = Field(default="")
