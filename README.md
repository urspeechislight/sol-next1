# sol-next1

A pipeline that transforms digitized classical Arabic manuscripts into a structured,
multilingual knowledge graph, plus the SvelteKit + FastAPI application scholars use to
explore it. Governed by an agent guardrail harness that enforces SSOT/DRY and hard
quality gates.

See [`docs/foundation.md`](./docs/foundation.md) for the mission and the data-integrity
stance that overrides everything else.

## Quick start

### Prerequisites

- **Node.js ≥ 22** (`.nvmrc` pins 22)
- **Python ≥ 3.10** at `python3` (`.python-version` pins 3.12; the agent
  harness hooks fail-closed on older Pythons)
- **pnpm ≥ 9** (via Corepack)
- **uv** for Python deps

```bash
# install toolchains (one-time)
corepack enable                   # for pnpm
curl -LsSf https://astral.sh/uv/install.sh | sh   # for uv
uv python install 3.12            # if your system python3 is < 3.10

# install deps
pnpm install
uv sync --group dev

# install git hooks
pnpm prepare

# run the frontend
pnpm dev

# run the backend (in another shell)
uv run uvicorn backend.main:app --reload --app-dir src
```

## Layout

| Path        | Purpose                                                    |
| ----------- | ---------------------------------------------------------- |
| `src/`      | All source code (frontend, backend, pipeline)              |
| `tests/`    | Python tests (mirrors `src/`)                              |
| `data/`     | Datasets, fixtures, samples                                |
| `docs/`     | All documentation                                          |
| `scripts/`  | Operational scripts                                        |
| `.claude/`  | Agent guardrail harness (control plane only)               |

See `docs/repo-layout.md` for the full structure and design rationale.

## Documentation

Every doc lives in [`docs/`](./docs/). Start with:

- [`docs/foundation.md`](./docs/foundation.md) — what this project is, what it isn't, why
- [`docs/repo-layout.md`](./docs/repo-layout.md) — folder conventions
- [`docs/design-system.md`](./docs/design-system.md) — SSOT design tokens and primitives
- [`docs/quality-standards.md`](./docs/quality-standards.md) — every rule the harness enforces
- [`docs/contributing.md`](./docs/contributing.md) — how to add code, run checks, ship a change
