"""FastAPI application entry point.

Wires routers, middleware, exception handlers, and the structured logger.
Keep this file thin — domain logic belongs in `services/`, transport in
`routers/`.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core import errors
from backend.core.config import get_settings
from backend.core.logging import configure_logging
from backend.routers import health

_log = structlog.get_logger(__name__)


@asynccontextmanager  # pyright: ignore[reportDeprecated]  -- contextlib.asynccontextmanager is the standard pattern; pyright stub deprecation flag is a false positive
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: startup + shutdown hooks."""
    settings = get_settings()
    configure_logging(settings.log_level, settings.log_format)
    _log.info("startup", env=settings.env, version=app.version)
    try:
        yield
    finally:
        _log.info("shutdown")


def create_app() -> FastAPI:
    """Application factory. Used by uvicorn and by tests."""
    settings = get_settings()
    app = FastAPI(
        title="sol-next1 API",
        version="0.1.0",
        docs_url="/docs" if settings.expose_docs else None,
        redoc_url="/redoc" if settings.expose_docs else None,
        openapi_url="/openapi.json" if settings.expose_docs else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    errors.install(app)
    app.include_router(health.router)
    return app


app = create_app()
