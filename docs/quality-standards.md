# Quality standards

Every rule the harness enforces, with rule IDs that match the structured
block envelopes you'll see in your terminal.

## Imports & boundaries

| Rule    | What it enforces                                                    |
| ------- | ------------------------------------------------------------------- |
| BND-001 | `$lib/design-system/internal/` is private to the design system      |
| BND-002 | Frontend may not import the `backend` or `pipeline` Python packages |
| ISO-001 | No references to sibling repos — sniffs paths, JS imports, and Python imports (`from akeyless import …` is also caught) |

## Design system

| Rule   | What it enforces                                                                |
| ------ | ------------------------------------------------------------------------------- |
| DS-001 | Raw color literals only in `tokens.css` (comments are stripped before scanning) |
| DS-002 | No inline styles: `style="..."`, unquoted `style=...`, `bind:style={...}`, or `el.style.X = ...` in scripts. Use `style:--token-name={value}` as the escape hatch. |
| DS-003 | Routes use design-system primitives, not raw `<button>`/`<input>` — including `<svelte:element this="button">` |
| DS-004 | Status / variant maps live only in `variants.ts` — flagged when ≥3 status-vocab keys appear in any object literal |
| DS-005 | No raw Tailwind arbitrary values for sizing (`text-[14px]`, `p-[3rem]`, `w-[200px]`). Use a token utility (`text-lg`, `p-4`) or `text-[length:var(--text-foo)]` |

## Code quality

| Rule     | What it enforces                                                  |
| -------- | ----------------------------------------------------------------- |
| QUAL-010 | File LOC: warn ≥ 300, block ≥ 500                                 |
| QUAL-011 | Function LOC ≤ 80 — Python via indent tracking, TS/JS/Svelte via brace matching |
| QUAL-012 | No bare `except:` or `except: pass`                               |
| QUAL-013 | No `print(` in `src/backend/` or `src/pipeline/` — use `structlog` |
| QUAL-014 | Magic numbers in production Python emit an advisory (allowed bare: `-1, 0, 1, 2, 100`; `constants.py` is exempt) |
| QUAL-020 | PostToolUse: ruff is run against the just-written Python file; failures emit advisory |
| PY-001   | Public Python functions need return-type annotations (`@overload` impl exempt) |

### Size caps

A file at 500 LOC almost always means too many responsibilities. The hard
cap is firm; the 300-LOC advisory is a reminder to start splitting.
Function caps are tighter — 80 LOC indicates the function is doing
multiple things or has accreted error-handling that should live elsewhere.

## Tests

| Rule     | What it enforces                                                  |
| -------- | ----------------------------------------------------------------- |
| TEST-001 | Test names: `test_should_<verb>_<object>_<condition>` (Python) or `should...` predicate (TS) |

A file is treated as a test file only when it lives under a `tests/`
directory or its stem starts with `test_` / ends with `.test` / `.spec`.
Files like `contest_helpers.py` are no longer false-matched.

**Python** test names must be `test_should_<verb>_<object>_<condition>` —
strict snake_case with at least three trailing segments. Example:
`test_should_return_404_when_user_not_found`.

**TS / JS** test names accept three styles, all starting with `should`
followed by a real predicate:

| Style       | Example                                       |
| ----------- | --------------------------------------------- |
| Snake       | `'should_render_button_when_loading'`         |
| Camel       | `'shouldRenderButtonWhenLoading'`             |
| Sentence    | `'should render button when loading'`         |

Bare `'should'`, generic names like `'renders correctly'`, or anything
without `should` as a prefix are blocked.

## Security

| Rule    | What it enforces                                                  |
| ------- | ----------------------------------------------------------------- |
| SEC-001 | High-confidence secret patterns blocked at write time. String concatenation (`'AKI'+'A...'`) is normalized before scanning |
| SEC-002 | Reads of obvious secret stores (`.env*`, `id_rsa`, etc.) blocked  |
| SEC-003 | Reads outside the repo emit advisory                              |
| SEC-004 | WebFetch to internal/loopback hosts (`localhost`, `*.internal`, link-local) blocked |
| SEC-005 | Every external fetch is logged to the audit trail                 |

The handler catches AWS keys, Google API keys, GitHub tokens, OpenAI /
Anthropic / Slack tokens, and PEM private-key headers. False positives
erode trust, so it's tuned conservatively. CI runs `gitleaks` for
authoritative scanning.

## Destructive commands

The PreToolUse:Bash handler refuses these without operator confirmation:

| Rule     | Pattern                                                                     |
| -------- | --------------------------------------------------------------------------- |
| BASH-001 | `rm -rf /` (or close) at filesystem root                                    |
| BASH-002 | `git push --force` to `main` / `master` in any flag order. `--force-with-lease` is allowed |
| BASH-003 | `git commit/push --no-verify`                                               |
| BASH-004 | `curl ... \| sh` (executing untrusted code)                                |
| BASH-005 | `git reset --hard`                                                          |

## Bash file writes

| Rule     | What it enforces                                                            |
| -------- | --------------------------------------------------------------------------- |
| BASH-100 | Bash file writes (`> file`, `tee`, `dd of=`, `sed -i`, `python -c "open()"`, `node -e "writeFile"`, `git apply`, `cp`/`mv`, `curl -o`, `wget -O`) targeting the project tree are blocked. Writes to `/tmp/`, `/var/tmp/`, `/dev/null` etc. remain allowed for diagnostics. |

This rule closes a major loophole: without it, an agent could `echo > foo.svelte`
and bypass the entire Write/Edit hook chain. Use the Write or Edit tool when
you need to create or modify a project file.

## Documentation

| Rule    | What it enforces                                                  |
| ------- | ----------------------------------------------------------------- |
| DOC-001 | Markdown lives in `docs/` (except root `README.md`, `CLAUDE.md`)  |
