"""Shared fixtures for unit tests (settings reset, TestClient without lifespan)."""

import os

import pytest
from fastapi.testclient import TestClient

from src.app import create_app
from src.configs.base_settings import BaseSettings
from src.di.dependency_container import configure_container, reset_container


@pytest.fixture(autouse=True)
def reset_settings() -> None:
    """Clear settings singletons and set minimal env for in-process tests."""
    os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-ci-only")
    os.environ.setdefault("JWT_ALGORITHM", "HS256")
    for name in (
        "AppSettings",
        {%- if cookiecutter.auth_mode == "jwt" %}
        "JWTSettings",
        {%- endif %}
        {%- if cookiecutter.has_postgres == "yes" %}
        "PostgresSettings",
        {%- endif %}
        {%- if cookiecutter.has_redis == "yes" %}
        "RedisSettings",
        {%- endif %}
        {%- if cookiecutter.has_telemetry == "yes" %}
        "TelemetrySettings",
        {%- endif %}
        {%- if cookiecutter.parichay_client == "yes" %}
        "ParichaySettings",
        {%- endif %}
        {%- if cookiecutter.abhilekh_client == "yes" %}
        "AbhilekhSettings",
        {%- endif %}
        {%- if cookiecutter.kavach_client == "yes" %}
        "KavachSettings",
        {%- endif %}
    ):
        BaseSettings._instances.pop(name, None)


@pytest.fixture
def client() -> TestClient:
    """In-process TestClient without lifespan (health liveness only; no live DB)."""
    reset_container()
    configure_container()
    return TestClient(create_app(), raise_server_exceptions=False)
