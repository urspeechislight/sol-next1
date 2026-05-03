"""Domain exception hierarchy + FastAPI error handlers.

The backend speaks one consistent error envelope::

    {"error": {"code": "snake_case_code", "message": "...", "detail": {...}}}

Domain exceptions inherit from `AppError`; the global handler maps them to
the right HTTP status. Pydantic validation errors and unhandled exceptions
get standardized too — clients should never see a stack trace.
"""

from __future__ import annotations

from typing import Any

import structlog
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

_log = structlog.get_logger(__name__)


class AppError(Exception):
    """Base class for all domain errors raised by the backend."""

    code: str = "app_error"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, detail: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or {}


class NotFoundError(AppError):
    """Resource lookup failed."""

    code = "not_found"
    status_code = status.HTTP_404_NOT_FOUND


class ValidationError(AppError):
    """Input data violated a domain invariant (distinct from Pydantic shape errors)."""

    code = "validation_error"
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


class ConflictError(AppError):
    """Operation conflicts with current resource state."""

    code = "conflict"
    status_code = status.HTTP_409_CONFLICT


def _envelope(code: str, message: str, detail: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the standard error envelope."""
    return {"error": {"code": code, "message": message, "detail": detail or {}}}


def install(app: FastAPI) -> None:
    """Register all error handlers on the app."""

    @app.exception_handler(AppError)
    async def _app_error(_request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, exc.message, exc.detail),
        )

    @app.exception_handler(HTTPException)
    async def _http_error(_request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope("http_error", str(exc.detail), {}),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=_envelope("invalid_request", "Request body failed validation", {"errors": exc.errors()}),
        )

    @app.exception_handler(Exception)
    async def _unhandled(_request: Request, exc: Exception) -> JSONResponse:
        _log.exception("unhandled_error", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope("internal_error", "An internal error occurred", {}),
        )
