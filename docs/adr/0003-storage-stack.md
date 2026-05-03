# ADR 0003 — Storage stack: Postgres + Neo4j

**Date:** 2026-05-02 **Status:** Accepted

## Context

The pipeline's terminal phase (Phase 5: GRAPH) produces a multi-domain knowledge
graph over the classical Arabic corpus: hadith and isnad, historical events and
participants, sectarian alignment (supporters of Ali / Ahl al-Bayt vs.
adversaries), tafsir, rijal, nahw, linguistics. Target scale is ~18,000 books
across 39 categories — order of magnitude **5M+ pages, tens of millions of
spans, ~100M+ edges, ~50M+ vector embeddings** at full extraction.

The hot queries are inherently hybrid:

> _Passages about Siffin (vector search) → narrated through chains containing at
> least one anti-Ali narrator (multi-hop graph path with property filter) →
> commented on in tafsir of verse X (cross-domain edge) → with rijal grading ≥ Y
> (property filter)._

This combines vector retrieval, multi-hop labeled-property-graph traversal, and
structured filters in a single logical query. The storage layer must serve all
three without forcing a cross-system join in application code.

Four candidate stacks were considered.

## Decision

Phase 5 writes to **two stores**:

- **Postgres** — authoritative source of truth for canonical text, page data,
  manuscript metadata, entity records, ORM-shaped relational data, migrations
  (Alembic), and audit. Anything that benefits from ACID and FK integrity lives
  here.
- **Neo4j** — the knowledge graph itself: nodes (Person, Event, Hadith, Verse,
  Span, Work, ...), edges (NARRATED_BY, ALIGNED_WITH, PARTICIPATED_IN, CITES,
  INTERPRETS_VERSE, ...), and **vector embeddings as node properties** indexed
  via Neo4j's native HNSW vector index. Vector search and graph traversal
  compose in a single Cypher query.

Postgres is the system of record. Neo4j is a _projection_ of the relational data
into graph-shaped form, rebuilt deterministically from Postgres if needed. Phase
5 is the only writer to Neo4j; the backend reads from both depending on the
query.

No Qdrant. No Redis by default (revisit only if a measured workload requires a
dedicated cache/queue that Postgres-based primitives cannot serve).

## Consequences

**Positive**

- **One graph engine, native to the workload.** Cypher's pattern syntax matches
  the multi-relation, multi-hop queries the domain demands.
  Recursive-CTE-in-Postgres at this edge-type diversity (dozens of edge kinds)
  gets unwieldy fast.
- **Vector + graph in one query.** Neo4j 5.x HNSW indexes let a Cypher query
  vector-search candidate nodes and traverse from them in one shot — no
  cross-system glue, no consistency window between the vector store and the
  graph.
- **Two stores, not four.** Drops Qdrant (replaced by Neo4j vector index) and
  Redis (not load-bearing at current scope). Halves the ops surface, backup
  story, and migration story versus the original four-store sketch.
- **Postgres remains the boring source of truth.** Migrations stay on Alembic.
  Pydantic + SQLAlchemy keep the data-integrity stance ("fail loudly, no silent
  fallbacks") enforceable at the type system.
- **Postgres survivability.** The corpus can be fully rebuilt from Postgres
  alone; the graph projection is reproducible.

**Negative**

- **Neo4j licensing requires attention.** Community Edition is GPLv3 and free;
  Enterprise is paid and unlocks clustering, role-based access, hot backups, and
  several graph algorithms. Single-instance Community covers the project until
  concurrent-write or HA needs appear. Budget the Enterprise question; do not
  assume Community forever.
- **Two stores, two consistency surfaces.** Postgres → Neo4j is a one-way
  derivation; Phase 5 writes the projection. Any drift is a bug, surfaced
  loudly. Out-of-band Neo4j writes are forbidden.
- **Two backup/restore stories.** Postgres via WAL + base backups; Neo4j via
  `neo4j-admin dump` (Community) or online backups (Enterprise). Recovery
  runbook must cover both.
- **Two query languages.** SQLAlchemy/SQL on the relational side, Cypher on the
  graph side. The backend service has to know when to use which. Rule:
  relational and ORM-shaped → SQL; multi-hop or pattern-shaped → Cypher.

## Alternatives considered

### Postgres only (with `pgvector` and recursive CTEs)

Rejected. At the original scope (isnad pipeline alone) this would have been
correct. At the actual scope — 39 categories, dozens of edge types, multi-domain
joins — recursive CTEs become long, slow, and hard to maintain. The simpler
stack stops paying off when the queries fundamentally want pattern-matching
syntax.

### ArangoDB (single multi-model store)

Rejected. Genuinely multi-model and operationally simpler in principle, but:

- Relicensed Apache 2.0 → BSL in 2023; license posture is a real risk for a
  long-lived project. Several features needed at 100M+ edges (SmartGraphs,
  encryption-at-rest, hot backup) are paywalled in Enterprise.
- Vector-search support is the youngest part of the engine (3.12+) — and vector
  retrieval is on the critical path.
- AQL has fewer training examples and a smaller ecosystem than SQL or Cypher;
  agent-generated code quality suffers proportionally. No Alembic-equivalent
  migration framework — a regression versus the Postgres tooling already wired
  up.
- Schema enforcement is opt-in, conflicting with the data-integrity stance.

The "good-enough at everything, best-in-class at nothing" tradeoff is not the
right one when the most demanding subsystem (vector search) is also the least
mature.

### Original four-store sketch (Postgres + Neo4j + Qdrant + Redis)

Rejected as the default. Defensible at scale, but Qdrant becomes redundant once
Neo4j's native HNSW is on the table, and Redis is speculative until a workload
demands it. Adding stores later is cheap; removing them is expensive.

### ruvector

Rejected. It is a vector database with grafted-on graph-flavored features, not a
labeled-property graph store. Production maturity is shaky (latest release is an
RC for an ESP32 sub-component), Python support is marginal (~0.5% of the
workspace), and the kitchen-sink scope (FPGA transformer, quantum coherence,
eBPF cognitive containers) is at odds with the boring-and-trusted storage layer
the data-integrity stance requires.

### Apache AGE (Cypher on Postgres)

Rejected for now. Tempting in principle (one engine, Cypher syntax), but
historically rough and slow-moving. Revisitable if maturity improves; not a
foundation to bet on today.

## References

- Neo4j vector indexes (v5+):
  <https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/>
- pgvector: <https://github.com/pgvector/pgvector>
- ArangoDB BSL announcement (2023):
  <https://arangodb.com/2023/09/business-source-license-bsl/>
- `docs/foundation.md` — data-integrity stance that constrains this choice
