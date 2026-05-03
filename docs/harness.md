# The harness

How the agent guardrails work end-to-end.

## Runtime requirement

Hooks run under the system **`python3` ≥ 3.10** (uses `dataclass(slots=True)`,
PEP 604 `X | Y` unions, parameterized generics). The shim
`.claude/hooks/_bootstrap.py` enforces this on every hook invocation — older
Python exits with code 2 and a clear message, blocking the tool call rather than
silently bypassing the guardrails (fail-closed).

To check or upgrade:

```bash
python3 --version          # must report 3.10 or newer
uv python install 3.12     # easiest path if too old
```

The hooks intentionally use the system Python (not `uv run python`) to keep
invocation latency low and avoid coupling to `uv sync` state. Handlers have zero
third-party deps for this reason.

## Architecture

```
                ┌────────────────────────┐
   tool call ──▶│  .claude/hooks/<event>.py │
                └─────────────┬──────────┘
                              │  reads JSON payload from stdin
                              ▼
                ┌──────────────────────────┐
                │  .claude/lib/dispatcher  │
                │   • build HookContext    │
                │   • run handlers in chain│
                │   • first deny wins      │
                │   • advisories accumulate│
                └─────────────┬────────────┘
                              ▼
                ┌──────────────────────────┐
                │  .claude/lib/handlers/   │
                │   each: ctx → Decision   │
                └─────────────┬────────────┘
                              ▼
                ┌──────────────────────────┐
                │  .claude/lib/audit       │
                │   append JSONL record    │
                └─────────────┬────────────┘
                              ▼
              exit 0 (allow) or exit 2 (block)
```

## Decision model

A handler returns one of:

- `Decision.allow()` — no opinion, continue chain.
- `Decision.advise(...)` — print warning, continue chain.
- `Decision.deny(...)` — block, end chain; first deny wins.

Decisions carry: `rule_id`, `handler`, `why`, `fix`, optional `doc` link. The
dispatcher emits a JSON envelope on stderr (machine-parseable) plus a
human-readable block citing rule + how to fix.

## Hook events wired

| Event                             | Dispatcher script        | Handlers run                                                                                                                                                                                                    |
| --------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SessionStart                      | `session_start.py`       | banner only                                                                                                                                                                                                     |
| UserPromptSubmit                  | `user_prompt_submit.py`  | (placeholder)                                                                                                                                                                                                   |
| PreToolUse: Write/Edit/MultiEdit  | `pre_tool_use_write.py`  | secret_scanner, external_refs, no_raw_colors, no_inline_styles, primitive_usage, variants_only, import_boundaries, no_silent_except, typed_python, function_size_cap, file_size_cap, test_naming, docs_location |
| PreToolUse: Bash                  | `pre_tool_use_bash.py`   | dangerous_bash                                                                                                                                                                                                  |
| PostToolUse: Write/Edit/MultiEdit | `post_tool_use_write.py` | (placeholder — extend with linter wrappers)                                                                                                                                                                     |

Handler order matters: cheap structural checks first, then content scans, then
size caps. The first deny in the chain blocks.

## Adding a handler

1. Create `.claude/lib/handlers/my_rule.py` exporting a
   `check(ctx) -> Decision`.
2. Add a corresponding entry in `.claude/policies/quality.yaml`.
3. Wire it into the relevant dispatcher (`pre_tool_use_write.py` etc.).
4. Add a test under `.claude/tests/test_my_rule.py`.
5. Document the rule in `docs/quality-standards.md`.

The handler MUST be:

- **Pure Python** — no LLM calls, no network.
- **Deterministic** — same input → same decision.
- **Fast** — well under 100 ms on a typical file.
- **Crash-tolerant** — exceptions are treated as denies (fail-closed).

## Audit log

Every decision (block, advisory, or allow that fired some checks) is appended as
a JSON line to `.claude/audit/events.jsonl`. The log is gitignored; ship it to
your telemetry of choice.

Each record:

```json
{
  "ts": 1714680000.123,
  "event": "PreToolUse:Write",
  "tool_name": "Edit",
  "session_id": "...",
  "blocked": true,
  "decisions": [{"severity": "block", "rule_id": "DS-001", ...}],
  "target": "/path/to/file.svelte"
}
```

## Self-tests

The harness has its own pytest suite under `.claude/tests/`. Run with:

```bash
uv run pytest .claude/tests
# or via the workspace alias
pnpm harness:test
```

CI runs this on every PR (`harness-self-test` job in
`.github/workflows/ci.yml`).

## Defense-in-depth

Three layers exist intentionally:

| Layer       | When                     | What it catches                       |
| ----------- | ------------------------ | ------------------------------------- |
| Agent hooks | pre/post agent tool call | bad code before it's even written     |
| Lefthook    | pre-commit / pre-push    | anything that slipped through; humans |
| CI          | every PR                 | the authoritative gate to merge       |

If a rule is in the harness, mirror it in CI. If a rule is in CI, consider
adding the cheaper version to the harness so the agent doesn't waste roundtrips
discovering it.
