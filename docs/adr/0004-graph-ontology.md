# ADR 0004 — Graph ontology: entities, edges, and controlled vocabularies

**Date:** 2026-05-02
**Status:** Accepted (framework); controlled-vocabulary fills tracked separately
**Supersedes the implicit ontology in:** none — predecessor project never settled this

## Context

The predecessor project (Python pipeline at `~/code/sol`) shipped Phases 1–3
but stalled at Phases 4–5 because **the ontology was never settled**. Specific
gaps the audit surfaced:

- No registry of valid entity types. `VALID_ENTITY_TYPES` was *referenced*
  in extractor code but never *defined*.
- No registry of valid edge types. The Phase 5 stub mentioned
  `CITES`, `HAS_SANAD`, `MENTIONS_PERSON`, `ALIGNS_WITH` in code comments;
  they never became schema.
- Sectarian alignment lived as a free-text property on the narrator
  record (`RijalEntry.stance`). No `Faction` / `Stance` node, no
  controlled vocabulary, no edge schema for Phase 5 to project against.
- Event participation roles were ad-hoc strings (`"shahid"`, `"qutila"`,
  `"with_ali"`) with no taxonomy.
- Rijal grading composed from per-narrator assessments to per-chain
  grades to cross-chain verdicts, but the composition wasn't pinned —
  chain grading leaked into Phase 3 (`extract.py:_apply_preliminary_chain_grades`).

The graph store is Postgres + Neo4j (ADR 0003). Neo4j is a labeled-property
graph, which means every node and edge carries a label. The labels need to
be *settled, registered, and validated* before Phase 5 code is written.
Otherwise we rebuild the same quagmire.

This ADR pins the **framework**: which entity types exist, which edge types
exist, how stance/alignment is modeled, how grading composes, and which
edges are valid between which entity types. Specific vocabulary values
(stance names, event types, role names, grading scales) are scholarly
calls — they're flagged as **Open vocabulary decisions** at the end and
tracked under Task #2.

## Decision

### 1. Entity types (the node taxonomy)

Every node in the graph carries exactly one *primary* type label drawn
from this registry. The registry lives in `config/sol.yaml` under
`entity_types:` and is validated at startup. New types require a
config change, not a code change.

| Type | Purpose | Identity |
|---|---|---|
| `Manuscript` | One physical/digital book; container of pages | URN |
| `Page` | One page of a manuscript | (manuscript_id, page_number) |
| `Span` | Structural text segment, the bridge between text and graph | UUID, links to source Page(s) |
| `Unit` | One atomic semantic unit extracted from a Span | UUID, links to Span |
| `Person` | Any human: narrator, scholar, historical figure, author. **One type, not many** | URN; merged across mentions via Phase 4 entity resolution |
| `Faction` | Controlled-vocabulary node for stance/alignment (singletons) | Stable ID from controlled vocab |
| `Event` | Historical event: battle, treaty, oath, martyrdom, debate | URN |
| `Place` | Geographic location | URN, lat/lon optional |
| `Verse` | Quranic verse | (sura, ayah) |
| `Hadith` | A logical tradition (matn + one-or-more sanads) | URN; canonical hash of matn |
| `Sanad` | A single isnad chain instance | UUID, child of one Hadith |
| `ChainDefect` | A defect attached to a Sanad (tadlis, irsal, ...) | UUID |
| `Work` | An abstract work (independent of manifestation/edition) | URN |
| `Root` | Arabic linguistic root (3- or 4-letter) | The root itself |
| `Lemma` | A canonical form / lexeme | URN, links to Root |

**One `Person` type for everyone.** Sol-next had `RijalEntry` and
`Person` drifting apart. A narrator who is also the subject of a
biography and a participant in an event is one node — narrator-ness,
biography-ness, and participation are *edges*, not types.

**`Faction` is a node, not a string.** This is the single most important
correction from sol-next. Stance and alignment are expressed as edges
to `Faction` nodes.

### 2. Edge types (the relation taxonomy)

The registry lives in `config/sol.yaml` under `edge_types:` with
declared `source_type` and `target_type`. Phase 5 validates every
edge against the registry before write. Out-of-registry edges raise.

**Structural** (deterministic, confidence = 1.0):

| Edge | From → To |
|---|---|
| `CONTAINS` | `Manuscript` → `Page` ; `Span` → `Span` (hierarchy) |
| `NEXT` | `Page` → `Page` ; `Span` → `Span` |
| `HAS_SECTION` | `Span` → `Span` (heading → body) |
| `HAS_FOOTNOTE` | `Span` → `Span` |
| `HAS_UNIT` | `Span` → `Unit` |
| `MANIFESTS` | `Manuscript` → `Work` |

**Hadith / isnad:**

| Edge | From → To | Properties |
|---|---|---|
| `HAS_SANAD` | `Hadith` → `Sanad` | — |
| `HAS_MATN` | `Hadith` → `Span` | — |
| `INCLUDES_NARRATOR` | `Sanad` → `Person` | `position: int` (0 = closest to source) |
| `NARRATES_FROM` | `Person` → `Person` | `evidence_anchor` (denormalized for fast traversal; primary truth lives on `Sanad.INCLUDES_NARRATOR`) |
| `HAS_DEFECT` | `Sanad` → `ChainDefect` | — |
| `PARALLEL_TO` | `Hadith` → `Hadith` | `confidence`, `alignment_method` |

**Person and stance:**

| Edge | From → To | Properties |
|---|---|---|
| `HAS_STANCE` | `Person` → `Faction` | `source_work_id`, `source_passage_id`, `confidence`, `evidence_anchor` |
| `STUDENT_OF` | `Person` → `Person` | source, evidence |
| `TEACHER_OF` | inverse of STUDENT_OF; do not store both — one direction only |
| `BIOGRAPHY_OF` | `Span` → `Person` | indicates this span is biographical material *about* the target |

A `Person` can have multiple `HAS_STANCE` edges from different sources;
they are not de-duplicated. Phase 5 emits one edge per assertion.
Aggregate stance (e.g. "majority of sources mark X as anti-Ali") is a
*query*, not a stored property.

**Events:**

| Edge | From → To | Properties |
|---|---|---|
| `PARTICIPATED_IN` | `Person` → `Event` | `role` (controlled vocab), `side` (controlled vocab; per-event side identifier), `outcome` (e.g. martyred, captured), `source`, `evidence_anchor` |
| `OCCURRED_AT` | `Event` → `Place` | — |
| `OCCURRED_IN_YEAR` | `Event` → integer year (Hijri) | property edge or property on Event — see §6 |
| `WITNESSED_BY` | `Event` → `Person` | mention-only, weaker than PARTICIPATED_IN |

Note: alignment-at-event (`side`) is **separate** from a person's general
`HAS_STANCE`. Someone may participate against Ali at one event and shift
allegiance later, or sources may document event-side without making a
general stance claim. Conflating these is a sol-next-style error.

**Tafsir, verse, linguistics:**

| Edge | From → To | Properties |
|---|---|---|
| `INTERPRETS_VERSE` | `Span` → `Verse` | (the span has tafsir behavior; this links it to the verse) |
| `REFERENCES_VERSE` | `Span` → `Verse` | weaker — verse mentioned, not interpreted |
| `HAS_LEMMA` | `Span` → `Lemma` | `position`, `confidence` |
| `HAS_ROOT` | `Lemma` → `Root` | — |

**Rijal grading (composition: per-narrator → per-chain → cross-chain):**

- *Per-narrator assessment* is an edge, not a node:
  `(:Person {role=scholar})-[:GRADED {term, grade_numeric, source_work_id, source_passage_id, evidence_anchor}]->(:Person {role=narrator})`.
  Many edges per narrator allowed; sources differ.
- *Per-chain grade* is properties on the `Sanad` node:
  `Sanad.grade`, `Sanad.weakest_position`, `Sanad.weakest_narrator_id`,
  plus `(:Sanad)-[:HAS_DEFECT]->(:ChainDefect)` edges. Computed in
  Phase 4 (ENRICH), **not** Phase 3.
- *Cross-chain verdict* is properties on the `Hadith` node:
  `Hadith.transmission_type`, `Hadith.epistemic_status`,
  `Hadith.corroboration_applied`. Aggregated from its `Sanad` children.

**Generic mention edges** (used during Phase 3 extraction, before
resolution to specific entities):

| Edge | From → To |
|---|---|
| `MENTIONS_PERSON` | `Span` → `Person` |
| `MENTIONS_EVENT` | `Span` → `Event` |
| `MENTIONS_PLACE` | `Span` → `Place` |
| `MENTIONS_VERSE` | `Span` → `Verse` |
| `CITES` | `Span` → `Hadith` ∣ `Span` → `Work` |

### 3. Edge-type registry contract

For each edge type, `config/sol.yaml` declares:
- `name`
- `source_types: [...]`  (allowed source labels)
- `target_types: [...]`  (allowed target labels)
- `multiplicity` (one-to-one ∣ one-to-many ∣ many-to-many)
- `directed: true` (always; we do not store inverses)
- `properties: { name: type }`  (allowed edge properties)

Phase 5 calls `validate_edge(edge, registry)` before every write. An edge
with an out-of-registry type, an out-of-registry source/target type, or
an unknown property raises `GraphSchemaError`. No silent coercion.

### 4. Stance / alignment model

```
(:Person)-[:HAS_STANCE {source_work_id, evidence_anchor, confidence}]->(:Faction)
```

`Faction` is a node with stable IDs from a controlled vocabulary (e.g.
`PRO_AHL_AL_BAYT`, `ANTI_AHL_AL_BAYT`, `AHL_AL_BAYT_MEMBER`,
`KHARIJI`, ... — final list under Open Decisions).

A person with five sources marking them anti-Ali has five
`HAS_STANCE` edges to `Faction(ANTI_AHL_AL_BAYT)`, each carrying the
attributing source. Aggregation (e.g. "consensus stance") is a Cypher
query, not a stored aggregate.

### 5. Event participation model

```
(:Person)-[:PARTICIPATED_IN {role, side, outcome, source, evidence}]->(:Event)
```

- `role`: enum from `participation_roles:` registry (e.g. `COMMANDER`,
  `COMBATANT`, `SIGNATORY`, `WITNESS`, `VICTIM`, `NEGOTIATOR`)
- `side`: enum from per-event `sides:` registry on the `Event` node
  itself (Battle of Siffin's sides are not the same as Karbala's).
  This is event-local, not corpus-global.
- `outcome`: enum (`MARTYRED`, `CAPTURED`, `WOUNDED`, `SURVIVED`, ...)

**Why `side` is event-local:** a global `with_ali`/`against_ali` taxonomy
breaks down the moment two events have orthogonal axes (Battle of the
Camel: Aisha vs Ali; Battle of Siffin: Mu'awiyah vs Ali — the two are
not the same `against_ali`).

### 6. Identity and merging

- `Person` deduplication is Phase 4's job, not Phase 3's. Phase 3
  produces *mention* `Person` candidates with provenance. Phase 4
  merges based on (kunya, nasab, death year, teacher overlap, ...) into
  canonical `Person` nodes.
- Until merged, mention candidates are distinct nodes labeled
  `Person` with a `mention_status: candidate | canonical | merged_into:<id>`
  property. Phase 5 only emits cross-domain edges from canonical
  candidates.
- `Event` identity is similarly deferred to Phase 4. Two mentions of "the
  Battle of Siffin" become one `Event` node post-merge.

### 7. Provenance is mandatory

Every non-structural edge carries:
- `source_work_id` (which work asserts this)
- `source_passage_id` (which passage)
- `evidence_anchor` (page, span, surrounding context)
- `extractor_id` (which extractor produced it)
- `confidence` (float ∈ [0, 1])

Edges missing any of these raise on write. This is the schema-level
expression of `foundation.md`'s "wrong is worse than absent."

### 8. Validation in Cypher (sample queries)

The schema is correct iff the project's hot queries are expressible.
Three representative queries — each must run in one Cypher statement:

```cypher
// Q1: Trace an isnad back through narrators.
MATCH (h:Hadith {urn: $hadith_urn})-[:HAS_SANAD]->(s:Sanad)
      -[r:INCLUDES_NARRATOR]->(p:Person)
RETURN s.id, r.position, p.canonical_name
ORDER BY s.id, r.position;

// Q2: Hadiths whose chains pass through any anti-Ali narrator.
MATCH (h:Hadith)-[:HAS_SANAD]->(s:Sanad)
      -[:INCLUDES_NARRATOR]->(p:Person)
      -[:HAS_STANCE]->(f:Faction {id: 'ANTI_AHL_AL_BAYT'})
RETURN DISTINCT h.urn, count(p) AS anti_ali_narrators_in_chain;

// Q3: Tafsir spans interpreting verses also cited in hadiths
//     about the Battle of Siffin.
MATCH (e:Event {urn: 'siffin'})<-[:MENTIONS_EVENT]-(:Span)<-[:HAS_MATN]-(h:Hadith),
      (h)-[:CITES_VERSE|MENTIONS_VERSE]->(v:Verse),
      (tafsir:Span)-[:INTERPRETS_VERSE]->(v)
RETURN h.urn, v.sura, v.ayah, tafsir.id;
```

If a hot query becomes unwieldy, that's a schema bug, not a query
problem — revisit the registry.

## Consequences

**Positive**

- Phase 5 has a target. Every edge it emits is validated against a
  registry; the alternative — sol-next's situation — is a stub that
  can't be written because nobody knows what to write.
- Stance and alignment are queryable, sourced, multi-asserted, and
  not free-text. The "find every transmission whose chain contains an
  anti-Ali narrator" query is one Cypher statement.
- Provenance on every edge is enforced at write time, not aspirational.
- One `Person` type unifies narrators, scholars, historical figures.
  No subtype proliferation.
- Event-side stays event-local. We never claim a global "with-Ali /
  against-Ali" axis that doesn't fit Karbala or Camel coherently.

**Negative**

- Two layers of registry (entity types + edge types) plus per-edge
  validation in Phase 5. More code than a free-form approach. This
  cost is what the predecessor *didn't* pay, and it's why it stalled.
- `Faction` as a node means stance changes require new
  `HAS_STANCE` edges rather than property updates. Acceptable — the
  history of stance assertions *is* scholarly content, not metadata.
- Sanad-as-node duplicates some information (chain narrators are
  reachable via `Person`-to-`Person` `NARRATES_FROM` edges too). We
  pay the duplication for chain identity, parallel detection, and a
  natural home for chain-level grade. `INCLUDES_NARRATOR` is
  authoritative; `NARRATES_FROM` is a denormalized projection rebuilt
  from it.
- Until Phase 4 entity resolution runs, mention-candidate `Person`
  nodes proliferate. Acceptable — the alternative is conflating
  unmerged mentions, which corrupts the graph.

## Alternatives considered

**Free-form labels (sol-next default).** Rejected. The predecessor's
quagmire is the proof. Without a registry, every extractor invents its
own labels and Phase 5 becomes unwriteable.

**Stance as a property on `Person`.** Rejected. Loses provenance,
loses multi-source assertions, loses the ability to query
"narrators stanced X by source Y." Sol-next's `RijalEntry.stance` had
provenance per assertion but no graph-level expression — exactly the
gap this ADR closes.

**Sanad-as-path (no Sanad node).** Considered. Pure-graph appeal: just
a sequence of `NARRATES_FROM` edges. Rejected because chain identity,
chain grade, chain defects, and parallel-chain detection all want a
*thing* to attach to. A path is not a thing.

**Subtype per role** (`Narrator`, `Scholar`, `HistoricalFigure`).
Rejected. Same person plays all three roles across the corpus.
Subtypes would force either duplication or fragile multi-label hacks.

**Global `side` taxonomy at participation** (`with_ali` /
`against_ali` / `neutral`). Rejected. Doesn't compose across events
with orthogonal axes (Camel, Siffin, Karbala). Per-event `sides:`
registry on the `Event` node itself is the correct shape.

## Vocabulary decisions — SETTLED 2026-05-02

The nine vocabulary questions are settled in `config/sol.yaml` with
primary-source grounding from the corpus (memory: `vocabularies_grounding.md`).
Two structural revisions emerged from the validation pass that materially
changed the model:

**Revision A — Alignment is a multi-axis registry, not a single faction.**
Classical scholarship treats theological school, juridical school,
political-dynastic loyalty, ahl-al-bayt stance, and spiritual orientation
as orthogonal. A Hanafi Maturidi Abbasid-loyalist neutral-on-ahl-al-bayt
Sufi person is internally consistent. Modeling these as one flat enum
would produce category errors. The five axes (`theological_school`,
`juridical_school`, `political_loyalty`, `ahl_al_bayt_stance`,
`spiritual_orientation`) live as separate registries in `config/sol.yaml`.
The five rijal-criticism categories Ibn Hajar names at Taqrib rank 5
(`tashayyu`, `qadar`, `nasb`, `irja`, `tajahhum`) are formally placed in
`theological_school` and `ahl_al_bayt_stance` as appropriate — they are
*formal rijal tags*, not project-coined polemics.

**Revision B — Narration attribution is not a chain defect.**
Per Ibn Hajar Nukhbat al-Fikr p.67 (sol_id `hQ2uVdeE` in the corpus),
`marfu` (chain to Prophet), `mawquf` (to Companion), `maqtu` (to Successor)
describe where a chain *terminates* — they are not problems with the chain.
Moved to a separate `narration_attribution` registry. A `mawquf` report can
be perfectly authentic *as a Companion-statement*; whether it counts as a
defect is a question downstream of the question being asked.

**Revision C — Manner of death and evaluative classification are separate axes.**
`Shahid` is a *source-relative evaluation*, not a manner of death.
Sunni and Shia sources disagree about who counts (e.g., ʿUthmān is `shahid`
in many Sunni sources and `maqtul` in many Shia ones). Modeling them as
parallel categories produces silent contradictions. Split into
`manner_of_death` (factual) and `evaluative_classification` (perspective-tagged).

**Revision D — Per-tradition rijal vocabularies, namespaced.**
`THIQA`, `HASAN`, `SAHIH` mean different things in Sunni vs Shia rijal
(Shia `SAHIH` requires all narrators to be Imami-Twelver; Sunni doesn't).
The `:GRADED` edge carries `tradition: SUNNI | SHIA | NEUTRAL` and the
term is validated against the per-tradition list. Pipeline code MUST not
collapse cross-tradition homonyms.

**Revision E — Transmission classes are two-tier, not flat.**
Top-level: `MUTAWATIR` vs `AHAD`. Sub-classification of AHAD by chain
count: `MUSTAFID` (>2; Ibn Hajar's primary term — Nukhbat p.16),
`MASHHUR` (alias of MUSTAFID in popularized usage), `AZIZ` (=2),
`GHARIB` (=1). GHARIB further splits into `FARD_MUTLAQ` (solo at root)
and `FARD_NISBI` (solo at some level) per Nukhbat p.20-21. Stored as
two properties on `:Hadith`: `transmission_class` and `count_class`.

**Other settled values (see `config/sol.yaml`):**
- 9 controlled-vocabulary registries grounded in primary corpus sources
- Sunni rijal grading: Ibn Hajar's authoritative 12-rank scheme from
  Taqrib al-Tahdhib intro pp. 24-25 (sol_id `qjQXdmB-_01`)
- Shia rijal grading: al-Hilli's binary i'timad/tawaqquf framing from
  Khulasat al-Aqwal p. 44 (sol_id `OzHS6N09`), supplemented by Najashi
- Narrator-defect causes: Ibn Hajar's canonical 10-item list from Nukhbat
  pp. 44-45
- Hadith verdict types from defects: 10+ values including the corpus-
  confirmed additions `mursal khafi`, `mukhtalit`, `musahhaf`, `muharraf`
- Event types: ~30 values including `mubahala`, `nass`, `tahkim`, `shura`,
  `bay'a`, `ghazwa`, `sariyya`, `dawa` — all classical event categories
- Hijri date granularity: `hijri_year` (int, required when temporal anchor
  exists), `hijri_month` (1-12, optional), `hijri_day` (1-30, optional),
  `year_uncertainty` (int, ± years), `source_date_text` (raw textual date
  from the source for provenance). No date-range types.
- Linguistic disciplines: settled. The Arabic linguistic sciences (nahw,
  sarf, balagha, 'arud, qafiya, lugha, fiqh al-lugha, ishtiqaq, aswat,
  khatt, insha, qira'a) and the balagha triad (ma'ani, bayan, badi') are
  registered as `linguistic_discipline` and `balagha_subdiscipline` in
  config/sol.yaml. [Source: al-Tahanawi, Kashshaf Istilahat al-Funun
  vol. 1 pp. 71-82 (sol_id `z_iqVsoq_01`).]
- Lexicon convention: settled. Arabic surface forms in the corpus map to
  canonical registry IDs via companion files at `config/lexicons/<domain>.yaml`.
  Each lexicon maps registry names to `{arabic_surface: canonical_id}`.
  `load_config` normalizes surface keys via `pipeline.utils.arabic.normalize_arabic`
  (NFC; strip tashkīl, kashida; normalize alif/hamza/yāʾ/tāʾ marbūṭa) at load
  time and validates referential integrity (every value must exist in the
  named registry). Runtime lookup is dict access. The pattern was chosen
  over structured-registry-entries (Option 3) after a parallel-agent design
  comparison; the lexicon shape handles semantic synonyms (مستور ≡ مجهول الحال)
  natively without schema gymnastics, lets migration be incremental as
  Phase 3 extractors come online, and keeps the existing `frozenset[str]`
  registry consumers unchanged. See memory: `lexicon_convention.md`.
- Tasawwuf (Sufism): settled. Four registries cover maqamat / aḥwāl
  (~50 stations/states with bab-page citations), `sufi_concept`
  (~30 technical terms), `nafs_stage` (the 7 stages of the lower self),
  and `sufi_tariqa` (17 historical Sufi orders). [Source: al-Qushayri,
  al-Risala al-Qushayriyya (sol_id `CB78uu0F`).]
- Kalam (theology): settled. Six registries cover sect-specific frameworks
  (`shia_usul_al_din` in shia_imamate.yaml; `sunni_arkan_al_iman`,
  `mutazili_usul_khamsa` in kalam.yaml), the canonical attribute lists
  (`sunni_sifat_al_maani`, `imami_sifat_thubutiyya`,
  `imami_sifat_salbiyya`), the cross-tradition topic registry
  (`kalam_topic` — ~40 recurring debates including divine-attribute
  problems, jabr/ikhtiyar, khalq al-Qur'an, ru'ya, shafaa, isma, etc.),
  and historical controversies (`kalam_controversy` — mihna, qadar,
  takfir, naṣṣ vs bayʿa, Ghadir, etc.). [Sources: al-Hilli, al-Bab al-Hadi
  ʿAshar (sol_id `yMuDJtbi`); al-Taftazani, Sharh al-Maqasid (sol_id
  `juyWaHEe`) and Sharh al-ʿAqaʾid al-Nasafiyya (sol_id `pozK-F7D`).]
- Fiqh registries: settled. Five registries cover legal theory and
  substantive law: `hukm_type` (the five ahkam: wajib, mandub, mubah,
  makruh, haram), `wajib_subtype` (ʿayni/kifaʾi, mudayyaq/muwassaʿ, etc.),
  `usul_source` (13 sources, with Sunni/Imami divergences flagged),
  `usul_al_fiqh_topic` (the four poles per al-Ghazali plus linguistic-
  indication and ijtihad/taqlid topics), and `furu_al_fiqh_chapter`
  (~60 substantive-law chapters in canonical ordering: ʿibadat →
  muʿamalat → munakahat → jinayat → qadaʾ → mawarith). [Sources:
  al-Ghazali, al-Mustasfa (sol_id `lYO3ynGb`); al-Shafiʿi, al-Risala
  (sol_id `NqavdhUN`); Mughniyya, al-Fiqh ʿala al-Madhahib al-Khamsa
  (sol_id `gcetLxeJ`).]
- Quranic sciences: settled. The 47 canonical categories (anwāʿ) of
  Quranic sciences from al-Zarkashi's al-Burhan fi 'Ulum al-Qur'an —
  spanning revelation history (asbab al-nuzul, makki/madani, jam'
  al-Qur'an), variant readings (qira'at, waqf wa ibtida, rasm), lexical
  (gharib, mu'arrab), verse structure (munasabat, fawasil), interpretive
  (tafsir, muhkam/mutashabih, nasikh/mansukh), rhetoric (i'jaz, amthal),
  legal (ahkam), and devotional (fada'il, adab al-tilawa) — are
  registered as `quranic_science`. [Source: al-Zarkashi, al-Burhan fi
  'Ulum al-Qur'an, 4 volumes (sol_id `oF_pDMSC`); each category cites
  its (volume:page) in config/sol.yaml.]
- Philosophical disciplines: settled. Mantiq (logic), falsafa, ilm ilahi
  (metaphysics), ilm tabi'i (natural philosophy), ilm riyadi (mathematics),
  hikma, ishraq, hikma muta'aliya, akhlaq are registered as
  `philosophical_discipline`. [Source: Kashshaf vol. 1 pp. 97-118.]
- Natural sciences: registered as `natural_science` (tibb, handasa, hai'a,
  nujum, miqat, zijat, 'adad, misaha, manazir, kimiya, falaha, firasa,
  ta'bir al-ru'ya). Most are minor for the hadith / event / tafsir KG but
  appear in the `arabic-language-sciences` and `logic-philosophy` corpus
  categories. [Source: Kashshaf vol. 1 pp. 110-118.]
- Per-discipline concept registries (specific nahw constructs, specific
  balagha tropes, specific logical figures) are deferred to per-extractor
  implementation work — the discipline registry is the right granularity
  for graph-level classification; finer concepts will be added when
  extractors for each discipline are implemented.

**Items deferred for specialist scholarly review:**
- al-Khoei's `Mu'jam Rijal al-Hadith` complete grading vocabulary (work
  not in corpus subset; rely on Hilli + Najashi until verified).
- Hanafi vs non-Hanafi treatment of `MUSTAFID` as a stricter sub-tier.
- Whether `wāqifī`/`fatḥī` are sect-modifiers (current choice) vs their
  own grading axis.
- Whether `tafarrud` is defect / flag / orthogonal property — currently
  omitted from `narrator_defect_cause`; classical practice (Ibn Hanbal)
  treats it as evidence/flag, not verdict.

## References

- ADR 0003 — storage stack (Postgres + Neo4j); this ADR sits on top
- `docs/foundation.md` — the data-integrity stance this schema enforces
- Predecessor evidence: `~/code/sol-next/src/models/__init__.py:264-274` (DegradedMode declared but unused), `src/phases/extract.py:454-483` (chain grading leaked into Phase 3), `src/phases/graph.py:6-24` (edge types in comments only)
- Memory: `sol_next_audit.md` — fuller list of predecessor lessons
