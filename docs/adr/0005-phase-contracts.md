# ADR 0005 — Phase contracts, degraded modes, and dependency discipline

**Date:** 2026-05-02
**Status:** Accepted

## Context

The predecessor pipeline at `~/code/sol-next` declared discipline it
never enforced. The audit (memory: `sol_next_audit.md`) surfaced four
load-bearing failures, all of the same shape — a contract written down
but not wired in:

1. **Phase contracts existed but were never validated.**
   `src/contracts.py` defined `validate_manuscript_for_phase()`. No phase
   ever called it. Every phase function silently trusted its input.
2. **`DegradedMode` enum existed but was never populated.**
   `src/models/__init__.py:264-274` declared the enum with seven
   members. `src/contracts.py:142-163` defined a degradation budget that
   gated expensive phases. No phase ever called
   `manuscript.degraded_modes.add(...)`. The budget gated against an
   always-empty set.
3. **Silent import-time fallbacks hid configuration bugs.**
   `src/phases/extract.py:48-52` does
   `try: from rijal import RijalClient; except: RijalClient = None`.
   A misconfigured rijal service cannot be told from a correctly-disabled
   feature. Both look like `RijalClient is None` at runtime.
4. **Phasing leak: chain grading lived in Phase 3.**
   `src/phases/extract.py:454-483` calls `_apply_preliminary_chain_grades()`.
   Chain grading is enrichment work — it depends on per-narrator rijal
   data, which is itself an enrichment input. It belongs in Phase 4.
   The leak made Phase 3 fail under conditions Phase 3 shouldn't care
   about.

ADR 0004 settled the *what* of the graph (entities, edges, controlled
vocabularies). This ADR settles the *how* of the pipeline — the
contracts each phase must honor and the discipline that keeps the
"fail loudly, no silent fallbacks" stance from `foundation.md`
enforceable instead of aspirational.

## Decision

### 1. Phase signature shape

Every phase is a single function with a typed signature:

```python
def phase_n(manuscript: Manuscript, config: Config) -> Manuscript:
    ...
```

- Input and output are the same `Manuscript` object, mutated in-place
  (kept from sol-next's working pattern — one Span type, populated
  progressively).
- The *contract* — which fields must be present on input, which fields
  the phase guarantees on output — is declared in
  `src/pipeline/contracts.py` as data, not as docstring prose.
- Phases are pure with respect to the input `Manuscript`. They mutate
  fields the contract names; they do not write to disk, network, or
  external services *except* as the phase's contract authorizes (e.g.,
  Phase 5 is the only authorized writer to Neo4j).

### 2. Mandatory contract validation at phase entry

The first executable line of every phase function is:

```python
def segment(manuscript: Manuscript, config: Config) -> Manuscript:
    validate_manuscript_for_phase(manuscript, "segment")
    ...
```

`validate_manuscript_for_phase()` checks the input contract:
- Required fields are populated.
- Required relationships hold (e.g., every Span belongs to a Page).
- The previous phase's `Manuscript.completed_phases` set includes the
  prior phase name.
- The degraded-mode budget for this phase has not been exceeded.

If any check fails, it raises `ContractError(phase, manuscript_id,
missing_invariant, ...)`. Not a warning. Not a log. The phase does not
run. The pipeline does not produce a "best-effort" Manuscript with a
half-populated graph.

A symmetric `validate_manuscript_after_phase(manuscript, "segment")`
runs at the end of each phase. If the phase's *output* contract is
violated, it raises before the Manuscript is handed to the next phase.

Validation is cheap (assertions over already-loaded data). The cost
is a few microseconds per phase. The benefit is that data-flow bugs
surface at the boundary they cross, not three phases later.

### 3. Phase purity rules

Each phase does one kind of work. Cross-phase work is the leak that
broke sol-next's Phase 3.

| Phase | Does | Does NOT |
|---|---|---|
| 1 INGEST | JSON → `Manuscript` with `Page`s, frontmatter classification, TOC parsing, metadata | No span analysis. No entity extraction. No graph writes. |
| 2 SEGMENT | Pages → Spans, FSM-driven hierarchy, pattern detection, behavior routing | No entity creation. No grading. No embedding. |
| 3 EXTRACT | Spans → Entities + Units. Mention-candidate Persons, Events, Verses, etc. with provenance. Run extractors per behavior. | **No grading** (chain or otherwise). No embedding. No translation. No entity resolution / merging. No graph writes. |
| 4 ENRICH | Translation, embedding, **chain grading**, **per-narrator rijal lookup**, entity resolution / canonicalization, cross-chain `HadithGrade` aggregation | No new entities (only resolves and grades existing ones). No graph writes. |
| 5 GRAPH | Mutates Neo4j: structural edges, citation resolution, cross-domain edges, `HAS_STANCE`/`PARTICIPATED_IN`/etc. per ADR 0004 registry | No new entities. No grading changes. No re-extraction. |

The chain grading rule deserves emphasis: **per-narrator rijal grades,
per-chain `Sanad` grades, and cross-chain `Hadith` verdicts are all
Phase 4.** Phase 3 produces a `Sanad` with an *unsanagraded* shape
and a `Hadith` with no transmission verdict. Chain defects are
identified in Phase 4, not Phase 3. This is the explicit fix for
sol-next's `extract.py:_apply_preliminary_chain_grades` leak.

Side-effect authorization (writes to anything outside the
`Manuscript`) is declared per phase:

| Side effect | Phases authorized |
|---|---|
| Read Postgres (manuscript metadata) | All |
| Write Postgres | 1 (manuscripts/pages), 4 (canonical entities, units), 5 (none — Postgres is updated *before* Phase 5) |
| Read Neo4j | 5 |
| Write Neo4j | 5 (only) |
| Call embedding API | 4 (only) |
| Call translation API | 4 (only) |
| Read rijal database | 4 (only) |

Out-of-band side effects raise `PhaseAuthorizationError`.

### 4. DegradedMode discipline

`DegradedMode` is an Enum in `src/pipeline/models.py`. Members
correspond 1:1 with named, recoverable degradations declared in
`config/sol.yaml` under `degraded_modes:`. Each member has:

- A short description
- The phase that may produce it
- Whether it disqualifies subsequent phases (and which)

**Every fallback path populates `manuscript.degraded_modes`.** No
exceptions. The pattern:

```python
try:
    rijal_data = rijal_client.lookup(narrator_id)
except RijalClientTransientError as e:
    log.warning("rijal_lookup_failed", narrator_id=narrator_id, exc_info=True)
    manuscript.degraded_modes.add(DegradedMode.RIJAL_UNAVAILABLE)
    manuscript.validation_issues.append(
        ValidationIssue(
            phase="enrich",
            kind="rijal_lookup_failed",
            narrator_id=narrator_id,
            cause=str(e),
        )
    )
    rijal_data = None  # explicit; downstream code checks
```

The contract validator at the start of Phase 5 checks the budget:

```python
# In config/sol.yaml:
phase_contracts:
  graph:
    requires_completed: [enrich]
    forbids_degraded: [TRANSLATION_FAILED]   # cannot graph without translations
    permits_degraded: [RIJAL_UNAVAILABLE]    # graph runs, edges marked low-confidence
```

A budget violation raises `DegradedBudgetExceededError`, naming the
phase, the offending degraded mode, and the manuscript id.

**Forbidden:** silently catching an exception and continuing. If a
fallback is taken, a `DegradedMode` is added; if no `DegradedMode`
applies, the exception propagates.

### 5. Dependency checks at config load, never at import

The audit's third failure (`try: from rijal import RijalClient;
except: RijalClient = None`) collapsed two distinct states into
one indistinguishable runtime check.

The rule: external dependencies are verified at config load, not at
import. `src/pipeline/config.py:load_config()` does:

```python
def load_config(path: Path) -> Config:
    config = parse_yaml(path)
    _validate_registries(config)   # entity types, edge types, factions
    _check_dependencies(config)    # rijal db, neo4j, postgres, embedding API
    return config
```

`_check_dependencies` performs a *liveness* probe — open a connection,
issue a no-op query, close — for each declared external service whose
feature flag is enabled. Failures raise `ConfigError` at startup, with
the offending service named.

This separates two real states:

- **Feature disabled** (`config.features.rijal: false`): import is
  skipped via feature flag; no liveness probe; no fallback.
- **Feature enabled, service down at startup**: `ConfigError` —
  the operator sees it immediately.
- **Feature enabled, service flapping mid-run**:
  `RijalClientTransientError` is caught at the call site; a
  `DegradedMode` is populated; the run continues per the budget.

`try/except ImportError: X = None` is forbidden in pipeline code. If
a module is conditional, gate the import on a config feature flag:

```python
if config.features.rijal_enabled:
    from src.pipeline.extractors.rijal import RijalClient  # noqa
```

### 6. Idempotency and determinism

Every phase is idempotent: running it twice on the same input
`Manuscript` produces the same output. This requires:

- Entity IDs are deterministic functions of content (e.g.,
  `uuid5(NAMESPACE_ENTITY, canonical_text + page + position)`). No
  `uuid4`, no `random`, no wall-clock timestamps in IDs.
- Phases use seeded sources of order (`sorted()` over Spans by
  `(page, offset, id)`), never iteration order over sets or dicts
  with insertion-order semantics that depend on input order.
- Phases that call non-deterministic external services (embedding,
  translation) cache outputs keyed by content hash. Re-running with
  cache hit is deterministic.

Idempotency makes backfills safe and tests reproducible. It is also
the precondition for the harness's "rebuild Neo4j projection
deterministically from Postgres" guarantee in ADR 0003.

### 7. Validation-gated progression (not full enforcement, but a place for it)

Sol-next had three validation-loop Markdown prompts because nobody
trusted pipeline output unattended. Sol-next1 keeps the *intent* —
per-phase accuracy gates — but builds them into the pipeline rather
than scattered prompts.

For each phase, `tests/pipeline/<phase>/golden/` holds golden
manuscripts with expected output. CI requires accuracy thresholds
declared in `config/sol.yaml` under `accuracy_thresholds:` (per phase,
per domain — e.g., `extract.hadith.precision >= 0.98`).

Phase-level test gates do *not* run at pipeline runtime — that would
be expensive and slow. They run in CI. A phase whose accuracy
threshold fails CI cannot ship.

This ADR establishes the contract; the actual gating mechanism is
implementation work tracked in a future task.

### 8. Test names follow the harness rule

`tests/pipeline/segment/test_segment.py::test_should_split_isnad_at_haddathana_boundary`
not `test_isnad_split`. The harness already enforces this (per
`docs/quality-standards.md`); this ADR notes it because pipeline tests
are where it bites hardest.

## Consequences

**Positive**

- Contracts are wired in. The audit's "declared but unused"
  scaffolding becomes load-bearing. A misconfigured pipeline fails at
  the boundary that's wrong, not three phases downstream.
- Phasing purity restored. Chain grading lives in Phase 4. Phase 3 is
  smaller, faster, and doesn't fail when a rijal service is down.
- Two distinct states ("feature disabled" vs "feature down") become
  distinguishable via `ConfigError` at startup. No more silent
  `RijalClient = None`.
- Degraded modes are observable. Every operator sees what was missing
  on every run, with the spans that triggered each degradation.
- Idempotency makes backfills and reprocessing safe. Re-running Phase
  3 over a corpus does not invent new entity IDs.
- Side-effect authorization gives a small, auditable surface. Only
  one phase writes Neo4j; only one calls the embedding API. Bugs
  in those calls cannot leak into other phases.

**Negative**

- More upfront code: `validate_manuscript_for_phase()`,
  `validate_manuscript_after_phase()`, the
  degraded-modes-in-config registry, the dependency liveness probe,
  the deterministic-ID utility. Estimated cost: ~150 lines of
  contract code in `src/pipeline/contracts.py`. The predecessor's
  `contracts.py` was 163 lines and didn't enforce; the equivalent
  here will be similar size and *will*.
- Idempotent IDs require care. `uuid5` over a canonical string is
  fine; the canonical string itself must be stable (whitespace
  normalization, encoding, ordering of fields). Bugs here produce
  duplicate "should-be-same" entities. Mitigated by tests that
  serialize → load → re-extract and assert ID equality.
- The "no try/except ImportError" rule is strict. Some Python
  libraries genuinely use that pattern (optional deps for a feature
  surface). We accept the rigidity in exchange for not reproducing
  the predecessor's bug.

## Alternatives considered

**Soft contracts (warnings, not errors).** Rejected. This is what
sol-next had de facto: contract code that didn't raise. The
predecessor's evidence is the rejection.

**Phase contracts as decorators** (`@phase("segment", requires=...)`).
Considered. More magical than `validate_manuscript_for_phase()` calls.
We kept the explicit call because it appears at the top of every phase
function — a constant reminder that the phase *has* a contract. A
decorator hides it.

**Pydantic models per phase** (separate types `IngestedManuscript`,
`SegmentedManuscript`, ...). Rejected for the same reason sol-next
rejected it: progressive `Manuscript` is the right shape, and per-phase
types create the "five frozen dataclasses" antipattern from the
original sol codebase. Contracts on a single `Manuscript` give the
same enforcement without the duplication.

**Catch-all `except Exception:` with logging.** Rejected.
`foundation.md` is explicit: "no silent suppression." A typed exception
caught at a known boundary is fine; a catch-all is a bug magnet.

## References

- ADR 0003 — storage stack
- ADR 0004 — graph ontology
- `docs/foundation.md` — data-integrity stance these contracts enforce
- Memory: `sol_next_audit.md` — the four predecessor failures this ADR addresses
- Predecessor evidence: `~/code/sol-next/src/contracts.py:142-163` (degradation budget against unpopulated set), `src/phases/extract.py:48-52` (silent import fallback), `src/phases/extract.py:454-483` (chain grading in Phase 3)
