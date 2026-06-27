"""Unit tests for {{cookiecutter.service_name}} health endpoint."""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch


@pytest.fixture
async def client():
    """Minimal app instance — no real infra started."""
    from src.app import create_app
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_health_simple(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_health_detailed_returns_structure(client: AsyncClient):
    response = await client.get("/health?detailed=true")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
