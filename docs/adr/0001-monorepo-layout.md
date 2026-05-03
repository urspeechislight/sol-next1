# ADR 0001 — Monorepo layout under `src/`

**Date:** 2026-05-02
**Status:** Accepted

## Context

We needed a folder structure for a multi-stack project (SvelteKit frontend,
FastAPI backend, Python data pipeline) with shared documentation. Two
mainstream conventions exist:

1. **Turborepo / Nx style** — `apps/` for deployable apps, `packages/` for
   shared libs.
2. **Single-app style** — one `src/` at the root containing everything.

The constraint from the project owner: a single `src/` at the root, with
sub-folders inside it (`frontend/`, `backend/`, ...). Plus, no doubled-up
`src/foo/src/` patterns when an app's framework has its own conventional
project root.

## Decision

- All source under `src/`. One subfolder per logical service:
  `src/frontend`, `src/backend`, `src/pipeline`. Add more as needed.
- `src/frontend/` is a SvelteKit project root (its own `package.json`,
  `svelte.config.js`, `vite.config.ts`). The internal `src/` that SvelteKit
  ordinarily uses is flattened via `kit.files.{routes,lib,params,...}`.
- Python services use **flat layout** (no per-service `src/` and no
  per-service `pyproject.toml`). One `pyproject.toml` at the repo root
  manages every Python package via Hatch + uv workspace.
- `tests/` mirrors `src/` for Python; frontend tests colocate.
- `docs/` is the only place Markdown docs (other than root README/CLAUDE) live.

## Consequences

**Positive**

- One `src/` at the top reads as "everything ships from here." Lower
  cognitive load.
- No `src/.../src/` nesting after the SvelteKit override.
- Single Python pyproject avoids per-service version drift; one `uv sync`
  installs the whole monorepo.

**Negative**

- Python services can't be published independently without re-extracting a
  per-service pyproject (acceptable — none of them are publish-targets
  today).
- Future contributors expecting `apps/` + `packages/` (Turborepo norm) need
  to read this ADR. Mitigated by `docs/repo-layout.md` being the first
  thing CLAUDE.md and README.md point at.
- Frontend keeps a small `package.json` inside `src/frontend/` because
  SvelteKit requires its own project root. This is *not* a duplicated
  `src/`; it's the framework's project boundary.

## Alternatives considered

- **`apps/` + `packages/`**: industry standard; rejected per owner preference.
- **Single Python package at the repo root, no `src/`**: would dilute the
  "everything in src" rule and make the frontend the odd-one-out.
- **Per-service pyproject (src-layout)**: rejected because it produces
  `src/backend/backend/` style nesting we explicitly want to avoid.

## References

- SvelteKit docs: <https://svelte.dev/docs/kit/configuration>
- PyPA src-vs-flat layout discussion: <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
- Tweag Python monorepo: <https://www.tweag.io/blog/2023-04-04-python-monorepo-1/>
