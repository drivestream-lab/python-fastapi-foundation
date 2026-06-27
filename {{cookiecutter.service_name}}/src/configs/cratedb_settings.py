"""CrateDB settings for {{cookiecutter.service_name}}."""

from typing import ClassVar
from pydantic import Field
from src.configs.base_settings import BaseSettings


class CrateDBSettings(BaseSettings):
    PREFIX: ClassVar[str] = "CRATE"

    host: str = Field(default="localhost")
    port: int = Field(default=4200)
    user: str = Field(default="crate")
    password: str = Field(default="")
    schema: str = Field(default="{{cookiecutter.service_name}}")
