# Contributing

## Prerequisites

| Tool   | Version        | Why                                                  |
| ------ | -------------- | ---------------------------------------------------- |
| Node   | ≥ 22 (LTS)     | SvelteKit 2 + Vite 6 baseline                        |
| pnpm   | ≥ 9            | Workspaces, deterministic installs                   |
| uv     | latest         | Python dep + venv management                         |
| python3| ≥ 3.10         | Harness hooks (`dataclass(slots)`, PEP 604 unions)   |

The harness fails-closed on older Python — install via
`uv python install 3.12` if your system `python3` is too old.

## One-time setup

```bash
corepack enable                                       # pnpm
curl -LsSf https://astral.sh/uv/install.sh | sh       # uv

pnpm install
uv sync --group dev
pnpm prepare                                          # installs lefthook
```

## Daily commands

```bash
pnpm dev              # frontend dev server (port 5173)
uv run uvicorn backend.main:app --reload --app-dir src   # backend dev (8000)
pnpm storybook        # design-system component sandbox (port 6006)

pnpm check            # frontend typecheck (svelte-check)
pnpm lint             # frontend ESLint
pnpm test             # frontend Vitest
pnpm test:e2e         # Playwright

pnpm py:check         # ruff + pyright
pnpm py:test          # pytest

pnpm ci               # everything (matches GitHub CI)
pnpm harness:test     # harness self-tests
```

## Workflow

1. Branch from `main`. Branch name `feat/<thing>` or `fix/<thing>`.
2. Make the change. The agent harness blocks rule violations as you go;
   read the block message — it tells you the rule, why, and how to fix.
3. `pnpm ci` locally before opening a PR.
4. Commit messages follow Conventional Commits (`feat: ...`, `fix: ...`).
   Lefthook's `commit-msg` hook enforces this.
5. Open the PR. CI runs the same checks again.

## Adding a feature

The order matters:

1. **If the feature needs new design tokens**, add them to
   `src/frontend/lib/design-system/tokens.css` first; mirror in `tokens.ts`.
2. **If the feature needs new variants**, add them to `variants.ts`.
3. **If the feature needs a new primitive**, add it under `primitives/`,
   add a story, export from `primitives/index.ts`.
4. **If the feature needs a new composed component**, add it under
   `composed/`, export from `composed/index.ts`.
5. **Then** wire it into a route. Routes consume primitives + composed only.

For backend changes, the analogous order: schema → service → router.

## Rules to know in advance

- All Markdown docs go in `docs/` (only `README.md` and `CLAUDE.md` may sit
  at root).
- No raw color literals outside `tokens.css`. No inline styles.
- Routes can't reach into `$lib/design-system/internal`.
- Test names: `test_should_<verb>_<object>_<condition>` (Python) or
  `should...` (TS).
- File ≤ 500 LOC, function ≤ 80 LOC.
- No bare `except:` / `except: pass`.

The full ruleset is in [`quality-standards.md`](./quality-standards.md).

## Disagreeing with a rule

The harness is strict by design, but it isn't infallible. If you genuinely
believe a rule is wrong:

1. Open a PR that updates `docs/quality-standards.md` and the corresponding
   handler (and its test).
2. Get the change reviewed — the harness change is the same as any code
   change.
3. **Do not** edit `.claude/policies/quality.yaml` to wave a single PR
   through.
