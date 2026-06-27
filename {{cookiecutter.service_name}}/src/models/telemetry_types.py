"""Telemetry type definitions for {{cookiecutter.service_name}}."""

from enum import Enum


class SpanStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
