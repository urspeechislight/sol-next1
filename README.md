# sol-next1

A pipeline that transforms ~18,000 digitized classical Arabic manuscripts across
39 disciplinary categories into a structured, multilingual knowledge graph, plus
the SvelteKit + FastAPI application scholars use to explore it. Governed by an
agent guardrail harness that enforces SSOT/DRY and hard quality gates.

The corpus spans the full breadth of classical Islamic scholarship: hadith and
rijal, tafsir and Qurʾanic sciences, fiqh across all major madhabs, kalam,
tasawwuf, sira and imamate, Arabic linguistic sciences (nahw / sarf / balagha /
ʿarud / lugha), falsafa and mantiq, medicine and natural sciences, history and
geography, biographical literature, poetry, and devotional works. **This is not
a hadith-only project** — fiqh is the largest domain by category count (12 of
the 39), and history + biography

- linguistics + ethics/sufism dominate the corpus by data mass.

## Read first

- [`docs/foundation.md`](./docs/foundation.md) — mission, scholarly use cases,
  the data-integrity stance that overrides everything else
- [`docs/corpus-scope.md`](./docs/corpus-scope.md) — authoritative inventory:
  the 7 domains, 39 categories, foundational works that ground each domain's
  vocabulary
- [`docs/adr/`](./docs/adr/) — architectural decisions (storage stack, graph
  ontology, phase contracts, frontend reader design, etc.)

## Quick start

### Prerequisites

- **Node.js ≥ 22** (`.nvmrc` pins 22)
- **Python ≥ 3.10** at `python3` (`.python-version` pins 3.12; the agent harness
  hooks fail-closed on older Pythons)
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

| Path       | Purpose                                       |
| ---------- | --------------------------------------------- |
| `src/`     | All source code (frontend, backend, pipeline) |
| `tests/`   | Python tests (mirrors `src/`)                 |
| `data/`    | Datasets, fixtures, samples                   |
| `docs/`    | All documentation                             |
| `scripts/` | Operational scripts                           |
| `.claude/` | Agent guardrail harness (control plane only)  |

See `docs/repo-layout.md` for the full structure and design rationale.

## Documentation

Every doc lives in [`docs/`](./docs/). Start with:

- [`docs/foundation.md`](./docs/foundation.md) — what this project is, what it
  isn't, why
- [`docs/corpus-scope.md`](./docs/corpus-scope.md) — authoritative inventory of
  the 7 domains and 39 categories
- [`docs/repo-layout.md`](./docs/repo-layout.md) — folder conventions
- [`docs/design-system.md`](./docs/design-system.md) — SSOT design tokens and
  primitives
- [`docs/quality-standards.md`](./docs/quality-standards.md) — every rule the
  harness enforces
- [`docs/contributing.md`](./docs/contributing.md) — how to add code, run
  checks, ship a change
