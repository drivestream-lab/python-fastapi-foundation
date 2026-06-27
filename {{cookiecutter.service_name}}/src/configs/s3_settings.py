"""S3 settings for {{cookiecutter.service_name}}."""

from typing import ClassVar, Optional
from pydantic import Field
from src.configs.base_settings import BaseSettings


class S3Settings(BaseSettings):
    PREFIX: ClassVar[str] = "S3"

    bucket_name: str = Field(default="{{cookiecutter.service_name}}-bucket")
    region: str = Field(default="ap-south-1")
    access_key_id: Optional[str] = Field(default=None)
    secret_access_key: Optional[str] = Field(default=None)
    endpoint_url: Optional[str] = Field(default=None)
