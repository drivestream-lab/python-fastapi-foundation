"""Kafka settings for {{cookiecutter.service_name}}."""

from typing import ClassVar, List
from pydantic import Field
from src.configs.base_settings import BaseSettings


class KafkaSettings(BaseSettings):
    PREFIX: ClassVar[str] = "KAFKA"

    bootstrap_servers: str = Field(default="localhost:9092")
    group_id: str = Field(default="{{cookiecutter.service_name}}-consumer")
    topics: List[str] = Field(default_factory=list)
    auto_offset_reset: str = Field(default="earliest")
    enable_auto_commit: bool = Field(default=False)
    session_timeout_ms: int = Field(default=30000)
    heartbeat_interval_ms: int = Field(default=10000)
    max_poll_records: int = Field(default=500)
