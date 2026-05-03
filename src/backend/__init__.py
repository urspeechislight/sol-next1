"""FastAPI backend service.

Provides the HTTP API consumed by the SvelteKit frontend (`src/frontend`).
Configuration lives in `backend.core.config`; route modules under
`backend.routers`. Service layer (domain logic) under `backend.services`.

Run with:
    uv run uvicorn backend.main:app --reload --app-dir src
"""

__version__ = "0.1.0"
