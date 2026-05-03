# Database migrations

Alembic, async SQLAlchemy, single migration history at `src/migrations/`.

## One-time bootstrap

```bash
uv sync --group dev
uv run alembic init src/migrations    # only if env.py doesn't already exist
```

The repo ships with `env.py` and `script.py.mako` already — there is nothing
to bootstrap.

## Generate a revision

Auto-detect changes against `backend.models`:

```bash
uv run alembic revision -m "add accounts table" --autogenerate
```

The new file lands at `src/migrations/versions/<timestamp>_<rev>_<slug>.py`.
Review it before committing — `--autogenerate` is a hint, not a contract.

## Apply

```bash
uv run alembic upgrade head        # apply everything
uv run alembic upgrade +1          # one step
uv run alembic downgrade -1        # roll back one
uv run alembic current             # current revision
uv run alembic history             # history
```

## Connection URL

Read from `Settings.database_url` (env var `SOL_DATABASE_URL`).
The `alembic.ini` value is a fallback for offline runs.

## Convention

- Every migration MUST have a working `downgrade()`. No one-way trains.
- Migrations are reviewed like code; never edit a migration once it's been
  applied to a shared environment.
- For data migrations, prefer a separate revision split (schema first, data
  second) so failures are recoverable.
