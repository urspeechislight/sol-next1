"""Health check endpoints. Used by load balancers and the harness CI."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from backend import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Liveness payload."""

    status: str
    version: str


@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    """Return service liveness. Always 200 when the process is up."""
    return HealthResponse(status="ok", version=__version__)


@router.get("/readyz", response_model=HealthResponse)
async def readyz() -> HealthResponse:
    """Return service readiness. Extend with downstream checks (DB, cache) as wired."""
    return HealthResponse(status="ready", version=__version__)
