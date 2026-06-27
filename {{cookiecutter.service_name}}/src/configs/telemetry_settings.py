"""OpenTelemetry settings for {{cookiecutter.service_name}}."""

from typing import ClassVar
from pydantic import Field
from src.configs.base_settings import BaseSettings


class TelemetrySettings(BaseSettings):
    PREFIX: ClassVar[str] = "OTEL"

    enabled: bool = Field(default=True)
    endpoint: str = Field(default="http://localhost:4318")
    service_name: str = Field(default="{{cookiecutter.service_name}}")
    export_interval_ms: int = Field(default=10000)
