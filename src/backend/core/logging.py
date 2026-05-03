"""Structured logging configuration.

Uses structlog with either JSON output (production) or pretty console output
(development). Application code obtains loggers via:

    import structlog
    log = structlog.get_logger(__name__)
    log.info("user.created", user_id=user.id)
"""

from __future__ import annotations

import logging
import sys
from typing import Literal

import structlog

LogLevel = Literal["debug", "info", "warning", "error", "critical"]
LogFormat = Literal["json", "console"]


def configure_logging(level: LogLevel, fmt: LogFormat) -> None:
    """Configure structlog + stdlib logging integration."""
    log_level = getattr(logging, level.upper())
    logging.basicConfig(stream=sys.stdout, level=log_level, format="%(message)s")

    processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    if fmt == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty()))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
