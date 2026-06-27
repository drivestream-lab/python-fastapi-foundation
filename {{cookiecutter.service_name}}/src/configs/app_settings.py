"""Application settings for {{cookiecutter.service_name}}."""

from enum import Enum
from typing import ClassVar
from pydantic import Field, field_validator
from src.configs.base_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGE = "stage"
    TESTING = "testing"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    PREFIX: ClassVar[str] = "APP"

    environment: Environment = Field(default=Environment.DEVELOPMENT)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default={{cookiecutter.default_port}})
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="text", description="'text' for dev, 'json' for prod")
    log_to_console: bool = Field(default=True)
    log_dir: str = Field(default="logs")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        u = v.upper()
        if u not in valid:
            raise ValueError(f"log_level must be one of {valid}")
        return u

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError("port must be between 1 and 65535")
        return v

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT
