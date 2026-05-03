"""Application settings.

Settings are loaded from environment variables via Pydantic Settings.
Read once at startup and cached; never reach for `os.environ` directly in
application code.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["debug", "info", "warning", "error", "critical"]
LogFormat = Literal["json", "console"]
Environment = Literal["dev", "test", "staging", "production"]


class Settings(BaseSettings):
    """Application settings loaded from env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SOL_",
        extra="ignore",
    )

    env: Environment = "dev"
    log_level: LogLevel = "info"
    log_format: LogFormat = "console"

    expose_docs: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sol"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings accessor. Use this everywhere instead of constructing Settings()."""
    return Settings()
