"""Async SQLAlchemy engine + session factory.

Wires the Postgres connection from `Settings.database_url`. Endpoints obtain
a session via the `get_db` dependency::

    from fastapi import Depends
    from backend.core.db import get_db

    @router.get(...)
    async def handler(db: AsyncSession = Depends(get_db)) -> ...:
        ...
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import get_settings


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Cached async engine. Created once per process."""
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=settings.env == "dev" and settings.log_level == "debug",
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Cached session factory bound to the engine."""
    return async_sessionmaker(get_engine(), expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: yield a session, commit on success, rollback on error."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
