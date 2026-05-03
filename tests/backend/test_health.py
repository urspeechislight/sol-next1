"""Health endpoint smoke tests."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import create_app


@pytest.mark.asyncio
async def test_should_return_ok_when_healthz_called() -> None:
    """`/healthz` returns 200 with `status=ok`."""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/healthz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"]


@pytest.mark.asyncio
async def test_should_return_ready_when_readyz_called() -> None:
    """`/readyz` returns 200 with `status=ready`."""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
