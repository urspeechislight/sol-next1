# Foundation

## What this project is

A pipeline that transforms ~18,000 digitized classical Arabic manuscripts across
39 disciplinary categories into a structured, searchable, multilingual knowledge
graph — together with the web application that lets scholars explore it. The
corpus spans the full breadth of classical Islamic scholarship: hadith and
rijal; tafsir and Qurʾanic sciences; fiqh across all major madhabs (Hanafi,
Maliki, Shafiʿi, Hanbali, Zahiri, Jaʿfari, Zaydi, Ismaili, Ibadi, plus
comparative); kalam (Sunni, Shia, Muʿtazili); tasawwuf; sira and imamate; Arabic
linguistic sciences (nahw, sarf, balagha, ʿarud, lugha); falsafa and mantiq;
medicine and natural sciences; history and geography; rijal and biographical
literature; poetry; and devotional works. See `docs/corpus-scope.md` for the
authoritative inventory.

The system targets queries that today require years of specialized training and
manual effort. A few representative scholarly use cases the knowledge graph
serves:

- **Hadith / rijal** — follow a hadith's isnad back through its narrators, trace
  parallel transmissions across collections, surface per-narrator grading from
  primary rijal works (Sunni: Ibn Hajar's Taqrib; Shia: al-Najashi, al-Hilli's
  Khulasat al-Aqwal), and discover which later scholars cited or commented on
  the same report.
- **Tafsir** — compare exegesis of a single Qurʾanic verse across Sunni and Shia
  tafsir traditions, with citations to the hadith and rijal authorities each
  commentator invokes.
- **Fiqh** — trace a single legal ruling (e.g., ablution prerequisites,
  inheritance shares, mutʿa marriage) across all five major madhabs and through
  their internal evolution, with links to the foundational texts and disputants.
- **Kalam** — follow a doctrinal concept (ʿisma, ghayba, divine attributes,
  khalq al-Qurʾan, walāya) across Imami, Muʿtazili, Ashʿari, and Maturidi
  treatments, with the historical controversies (mihna, qadar debate, naṣṣ vs
  bayʿa) that shaped each position.
- **Tasawwuf** — map the maqamat / aḥwāl through al-Qushayri's _al-Risāla_,
  al-Hujwiri's _Kashf al-Mahjub_, al-Suhrawardi's _ʿAwārif_, and trace which
  Sufi ṭuruq trace their silsila through which historical shaykhs.
- **Sira / Imamate** — reconstruct the historiography of an event (Ghadir Khumm,
  Karbala, Siffin, Mubahala) across hostile and sympathetic sources, surfacing
  each narrator's stance and the chains through which the report reached the
  compiler.
- **Linguistic sciences** — trace a grammatical concept (i'rab, idafa,
  particles, broken plurals) through nahw and sarf works, or follow a rare
  Quranic word (gharib al-Qurʾan) through the lexicographic tradition (Lisan
  al-ʿArab, Tahdhib al-Lugha, al-Qamus).

Today none of these is possible without years of specialized knowledge and
manual cross-referencing across hundreds of works. This system makes it possible
— at scale, across the entire corpus.

## The architecture: five phases plus an application

The codebase has three deployable units, all governed by one agent guardrail
harness:

**`src/pipeline/`** — a five-phase Python pipeline that turns manuscript JSON
into knowledge-graph edges:

```
Phase 1: INGEST    — JSON → normalized pages + metadata
Phase 2: SEGMENT   — pages → labeled spans + hierarchy
Phase 3: EXTRACT   — labeled spans → entities + atomic units
Phase 4: ENRICH    — units → translations + embeddings
Phase 5: GRAPH     — everything → knowledge graph edges
```

Each phase is a function with a declared input type and output type. The domain
knowledge — Arabic patterns, behavior routing rules, entity types, graph schema,
every numeric threshold — lives in configuration. Python executes it.

**`src/backend/`** — a FastAPI service that exposes the graph over HTTP: search,
traversal, citation lookup, narrator chains, the queries scholars actually run.

**`src/frontend/`** — a SvelteKit application that lets scholars query and
browse the graph. Tokens, primitives, and variants are centralized so the
surface stays coherent as it grows.

## Data integrity is non-negotiable

This is production software processing irreplaceable scholarly data. The
following stance is absolute and overrides any other instinct toward
convenience.

**Fail loudly, always.** A phase that cannot produce correct output raises. It
does not return a plausible-looking wrong answer. A wrong narrator extraction, a
spurious citation edge, a mislabeled span — each actively harms the scholar who
trusts it. Wrong is worse than absent.

**No silent suppression.** No bare `except:`, no `except Exception: pass`, no
`or "UNKNOWN"` fallbacks in error paths. Every exception is logged with full
context and either re-raised or converted to a typed error. The harness blocks
the patterns; the philosophy is what makes the rule make sense.

**Structural errors are bugs, not edge cases.** If a phase encounters state it
does not expect, that is a bug in the config or the input — not a recoverable
situation. Fix the source. Do not patch the symptom with a default.

**When uncertain, produce nothing and log why.** Uncertainty is not a reason to
invent. An empty result the scholar can investigate is always better than a
confident wrong one they cannot.

## What this project is **not**

- Not a derivative of any other project. The folder is unconnected to any
  sibling directory on this machine by reference, import, copied content, or
  configuration. Every file is original.
- Not a starter kit you customize and forget. The harness is meant to remain
  active as the project grows; it gets stricter, not weaker.
- Not language-or-framework agnostic. The choices are committed: SvelteKit,
  Svelte 5 runes, Tailwind 4, TypeScript strict, FastAPI, Pydantic v2, uv, Ruff,
  Pyright. Pick something else and you are forking.

## Standalone contract

Every element of this codebase appears designed from scratch in isolation of
every other project on this machine. Concretely:

1. **No imports** that resolve outside this repo (other than published
   packages).
2. **No paths** referencing sibling project directories (e.g.
   `../some-other-repo/...`, `~/code/another-project/...`). The harness handler
   `external_refs` blocks these on write.
3. **No copied content** — file contents are original, even when the patterns
   they implement were observed elsewhere.

If you ever feel the temptation to "just borrow that one file from a neighboring
project," stop. Re-implement it.

## Why an agent harness

A harness is not a linter. It is the _control plane_ — a layer of pre/post
tool-use hooks that observe and decide on every write the agent makes, before
the file lands. It complements (does not replace) developer-side checks
(lefthook, ruff, eslint) and CI:

| Layer       | When it runs             | Strength       |
| ----------- | ------------------------ | -------------- |
| Agent hooks | Pre/post agent tool call | Fast, surgical |
| Lefthook    | pre-commit / pre-push    | Cheap, local   |
| CI          | every PR                 | Authoritative  |

The three layers catch different mistakes. The harness catches the agent during
generation, before bad code is even written; lefthook catches anything that
slipped through and a human is about to commit; CI is the source of truth that
gates merge.

The harness is especially load-bearing here because the domain rewards
discipline: silent fallbacks corrupt a knowledge graph in ways that are
invisible until a scholar trusts a wrong connection. The harness is one of the
mechanisms that keeps the data-integrity stance above from eroding under
deadline pressure.

## Long-term thesis

Codebases rot when each new file makes its own micro-decisions about color,
naming, error handling, file size, and import boundaries. The harness exists to
keep those micro-decisions centralized: one tokens file, one variants registry,
one rule for size, one boundary policy. Every contributor (human or agent) plays
inside that fence — so that five years from now the codebase still reads like
one mind wrote it, and the data the pipeline produces can still be trusted.
