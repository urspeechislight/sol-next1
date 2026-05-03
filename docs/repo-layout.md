# Repository layout

## Tree

```
sol-next1/
├── src/                       # ALL source code lives here
│   ├── frontend/              # SvelteKit project root (own package.json + config)
│   │   ├── routes/            # SvelteKit pages / endpoints
│   │   ├── lib/               # importable via $lib
│   │   │   ├── design-system/ # tokens, primitives, composed (the SSOT layer)
│   │   │   ├── stores/        # Svelte stores (theme, prefs, ...)
│   │   │   └── server/        # server-only helpers (api-client, etc.)
│   │   ├── params/            # route param matchers
│   │   ├── static/            # public assets
│   │   ├── app.html           # HTML shell
│   │   ├── app.css            # global stylesheet entry (imports tokens.css)
│   │   ├── error.html         # error shell
│   │   ├── hooks.client.ts
│   │   ├── hooks.server.ts
│   │   ├── svelte.config.js   # configures kit.files to flatten the source layout
│   │   └── package.json       # SvelteKit needs its own project root
│   ├── backend/               # FastAPI service (Python package: `import backend`)
│   │   ├── core/              # config, logging, db session, errors
│   │   ├── models/            # SQLAlchemy ORM
│   │   ├── routers/           # transport (one file per resource)
│   │   ├── services/          # domain logic (transport-agnostic)
│   │   └── main.py            # FastAPI app factory
│   └── pipeline/              # heavy-compute pipeline (Python package)
│
├── tests/                     # mirrors src/ for Python tests
│   ├── backend/
│   └── pipeline/
│
├── data/                      # samples, fixtures, seeds (gitignored where appropriate)
├── docs/                      # ALL documentation (this is the only place .md files live)
├── scripts/                   # operational scripts
│
├── .claude/                   # the harness — control plane only
│   ├── settings.json          # hook event registration
│   ├── hooks/                 # entry-point dispatchers (called by Claude Code)
│   ├── lib/                   # importable handler library
│   │   └── handlers/          # one file per quality rule
│   ├── policies/              # declarative ruleset (YAML)
│   ├── tests/                 # harness self-tests
│   ├── state/                 # cached state (gitignored)
│   └── audit/                 # JSONL audit log (gitignored)
│
├── .github/workflows/         # CI pipelines
├── package.json               # pnpm workspace root
├── pnpm-workspace.yaml
├── pyproject.toml             # uv workspace root (single Python pyproject)
├── lefthook.yml               # developer git hooks
├── README.md                  # entry — points here
└── CLAUDE.md                  # entry for the agent — points here
```

## Conventions

### `src/`

- One sub-folder per logically deployable unit (`frontend`, `backend`,
  `pipeline`, ...). Add new ones as the system grows; do not nest deployment
  units (no `src/services/api/...`).
- `frontend/` keeps a flat internal layout — no inner `src/` — by overriding
  `kit.files.routes`, `kit.files.lib`, etc. in `svelte.config.js`.
- Python packages under `src/` have flat layout (no inner `src/`). They share
  the workspace `pyproject.toml` at the repo root. If a service ever needs to
  be extracted into its own publishable package, that extraction is the moment
  to switch *that one* to a per-service pyproject.

### `tests/`

- Python tests live here, mirroring `src/`.
- Frontend tests colocate next to source (`Component.test.ts`) — Vitest
  convention. Don't move them.
- E2E tests live in `src/frontend/e2e/`.

### `docs/`

- Every Markdown doc except the root `README.md` and `CLAUDE.md` lives here.
  The harness handler `docs_location` blocks writes that violate this.
- Architecture decisions go in `docs/adr/NNNN-title.md`.

### `data/`

- Treat as ephemeral by default. Anything reproducible from the pipeline
  shouldn't be committed; commit only fixtures small enough to be useful for
  tests.

### `.claude/`

- The harness is the control plane. It must not contain application code.
- Hooks in `.claude/hooks/` are entry points only; logic is in `.claude/lib/`.
- Do not add per-feature exceptions to handlers — if a rule is wrong, fix the
  rule (and its test) deliberately, with a doc PR.

## Why this shape

- Single `src/` matches user preference and avoids the `apps/`/`packages/`
  duality of a Turborepo while still working with pnpm + uv workspaces.
- Per-app project roots inside `src/` (frontend has its own `package.json`)
  are unavoidable for SvelteKit; the framework expects its own root. We
  flatten everything *inside* it via `kit.files`.
- Tests mirror `src/`, not colocate, because Python idiom favors
  out-of-tree tests; Vitest in the frontend favors colocation. Both are
  honored where they belong.
- All docs in one place keeps cross-references trivial and the rest of the
  tree free of stray Markdown.
