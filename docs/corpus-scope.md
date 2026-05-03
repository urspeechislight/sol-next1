# Corpus scope

The authoritative inventory of what this project covers. Anyone learning
the codebase should read this before assuming the project is narrowly
about hadith — the corpus is much broader.

## Numbers

- **~18,000 books** in the full corpus
- **~20 GB** of JSON content (frontmatter + TOC + page-level Arabic text)
- **39 disciplinary categories**
- **189 books / ~38 MB** in the development subset (committed lifecycle:
  gitignored at `data/books/`; full corpus is loaded at runtime from a
  configurable path)

The 39 categories are not balanced by mass. By data size, the four
largest categories (history-geography, prophet-imams-biography,
arabic-language-sciences, genealogy-biography) account for over 5 GB —
roughly 25% of the corpus. Hadith categories are scattered across seven
slots and individually mid-sized. **Categorizing this project as
"a hadith pipeline" misrepresents the scope.**

## Domains and categories

The 39 categories partition into 7 scholarly domains. Below, each domain
includes its categories (with the directory slug used in `data/books/`),
a one-sentence description, and the foundational classical works that
ground the controlled vocabularies in `config/shards/`.

### 1. Hadith Sciences (7 categories)

The transmitted reports of the Prophet, the Imams (in Shia tradition),
and the Companions, plus the methodological literature (mustalah
al-hadith) and biographical literature on narrators (rijal).

| Category | Description |
|---|---|
| `sunni-hadith-general` | The six Sunni canonical collections (Bukhari, Muslim, Tirmidhi, Nasaʾi, Abu Daʾud, Ibn Maja) and broader compilations |
| `sunni-hadith-fiqh` | Hadith works oriented at legal derivation |
| `sunni-hadith-narrators` | Sunni rijal: Ibn Hajar's Taqrib al-Tahdhib, Tahdhib al-Tahdhib, Lisan al-Mizan, al-Isaba; al-Dhahabi's Mizan al-Iʿtidal |
| `shia-hadith-general` | Shia hadith collections: al-Kafi, Man la Yahduruhu al-Faqih, Tahdhib, Istibsar (al-Kutub al-Arbaʿa); al-Wafi; Wasaʾil al-Shiʿa; Bihar al-Anwar |
| `shia-hadith-fiqh` | Shia hadith works oriented at legal derivation |
| `shia-hadith-narrators` | Shia rijal: al-Najashi's Rijal, al-Tusi's Fihrist and Rijal, al-Kashshi's Ikhtiyar Maʿrifat al-Rijal, al-Hilli's Khulasat al-Aqwal, al-Mamaqani's Tanqih al-Maqal |
| `fiqh-terminology` | Cross-domain dictionaries of legal/hadith technical terms (al-Tahanawi's Kashshaf, etc.) |

Foundational source for the hadith vocabulary in `config/shards/hadith.yaml`:
**Ibn Hajar al-ʿAsqalani, Nukhbat al-Fikr fi Mustalah Ahl al-Athar**
(sol_id `hQ2uVdeE`).

### 2. Qurʾanic Sciences (3 categories)

Tafsir (exegesis), variant readings (qiraʾat), the disciplines of ʿulum
al-Qurʾan (47 anwāʿ per al-Zarkashi).

| Category | Description |
|---|---|
| `sunni-tafsir` | Sunni exegesis: al-Tabari, Ibn Kathir, al-Qurtubi, al-Razi, al-Zamakhshari, al-Suyuti |
| `shia-tafsir` | Shia exegesis: al-Tabarsi (Majmaʿ al-Bayan), al-Qummi, al-ʿAyyashi, al-ʿAllama al-Tabatabaʾi (al-Mizan) |
| `quran-sciences` | The methodological literature: asbab al-nuzul, makki/madani, nasikh wa-mansukh, iʿjaz, etc. |

Foundational source: **al-Zarkashi, al-Burhan fi ʿUlum al-Qurʾan** (sol_id
`oF_pDMSC`) — the canonical pre-Suyuti taxonomy of 47 anwāʿ.

### 3. Fiqh / Jurisprudence (12 categories — the largest domain by category count)

Substantive law (furuʿ) and legal theory (usul al-fiqh) across all major
madhabs.

| Category | Description |
|---|---|
| `hanafi-fiqh` | Hanafi madhab |
| `maliki-fiqh` | Maliki madhab |
| `shafii-fiqh` | Shafiʿi madhab |
| `hanbali-fiqh` | Hanbali madhab |
| `zahiri-fiqh` | Zahiri madhab (Ibn Hazm tradition) |
| `zaidi-fiqh` | Zaydi Shia madhab |
| `shia-fiqh-pre-8th-century` | Imami fiqh through the 7th century AH |
| `shia-fiqh-8th-century` | Imami fiqh of the 8th-century AH (al-Hilli era) |
| `shia-fiqh-fatwas` | Imami fatwa collections |
| `shia-fiqh-principles` | Imami usul al-fiqh: al-Tusi, al-Hilli, modern (Khurasani, Naʾini) |
| `sunni-fiqh-principles` | Sunni usul al-fiqh: al-Shafiʿi's Risala, al-Ghazali's Mustasfa, al-Amidi, al-Razi |
| `independent-fiqh` | Comparative / non-aligned works (Mughniyya's al-Fiqh ʿala al-Madhahib al-Khamsa) |

Foundational sources for `config/shards/fiqh.yaml`:
**al-Ghazali, al-Mustasfa min ʿIlm al-Usul** (sol_id `lYO3ynGb`) for the
four-pole structure of usul al-fiqh; **Mughniyya, al-Fiqh ʿala
al-Madhahib al-Khamsa** (sol_id `gcetLxeJ`) for the canonical chapter
structure of furuʿ across madhabs.

### 4. Theology and Sects (3 categories)

Kalam (rationalist theology), creed exposition, polemics across sects.

| Category | Description |
|---|---|
| `sunni-theology` | Ashʿari and Maturidi kalam; al-Taftazani (Sharh al-Maqasid, Sharh al-ʿAqaʾid al-Nasafiyya), al-Iji (al-Mawaqif), al-Razi |
| `shia-theology` | Imami kalam: al-Mufid (Awaʾil al-Maqalat), al-Tusi (Tajrid al-Iʿtiqad), al-Hilli (al-Bab al-Hadi ʿAshar, Manahij al-Yaqin), Mulla Sadra |
| `sects-schools` | Heresiographies and sectarian polemics |

Foundational sources for `config/shards/kalam.yaml` and
`shards/shia_imamate.yaml`: **al-Hilli, al-Bab al-Hadi ʿAshar** (sol_id
`yMuDJtbi`); **al-Taftazani, Sharh al-Maqasid** (sol_id `juyWaHEe`).

### 5. Biography and History (3 categories)

The historiographic and biographical literature — by data mass the
largest domain in the corpus.

| Category | Description |
|---|---|
| `history-geography` | Universal histories (al-Tabari, Ibn al-Athir, al-Yaʿqubi, Ibn Khaldun), regional histories, geographies |
| `prophet-imams-biography` | Sira (life of the Prophet) and biographies of the Twelve Imams (al-Mufid's al-Irshad, al-Tabarsi's Iʿlam al-Wara, al-Majlisi's Bihar al-Anwar volumes on the Imams) |
| `genealogy-biography` | Tabaqat literature (Ibn Saʿd's al-Tabaqat al-Kubra), prosopographical compendia, ansab works |

Foundational source for `shards/masumin.yaml` (the canonical 14
Maʿsumin): **al-Mufid, al-Irshad fi Maʿrifat Hujaj Allah ʿala al-ʿIbad**.

### 6. Sciences (4 categories)

Linguistic sciences, philosophy and logic, medicine, and other classical
sciences.

| Category | Description |
|---|---|
| `arabic-language-sciences` | Nahw (Sibawayh's Kitab, Ibn Malik's Alfiyya, Ibn Hisham's Mughni al-Labib); sarf; balagha (al-Sakkaki, al-Qazwini, al-Jurjani); ʿarud; lugha (Lisan al-ʿArab, al-Sihah, al-Qamus) |
| `logic-philosophy` | Mantiq, falsafa, hikma; al-Farabi, Ibn Sina, al-Suhrawardi, Ibn Rushd, Mulla Sadra |
| `medicine` | Tibb: Ibn Sina's al-Qanun, al-Razi, traditional Islamic medicine |
| `other-sciences` | Astronomy, geometry, mathematics, optics, and other classical sciences |

Foundational source for `shards/disciplines.yaml`: **al-Tahanawi, Mawsuʿat
Kashshaf Istilahat al-Funun wa al-ʿUlum** (sol_id `z_iqVsoq_01`) — the
authoritative encyclopedia of technical terms across all classical
Islamic disciplines.

### 7. Devotional and Other (7 categories)

Tasawwuf, devotional works, poetry, and meta-bibliographic works.

| Category | Description |
|---|---|
| `ethics-mysticism` | Tasawwuf and akhlaq: al-Qushayri's Risala, al-Sarraj's Lumaʿ, al-Hujwiri's Kashf al-Mahjub, al-Suhrawardi's ʿAwarif, al-Ghazali's Ihyaʾ; Sufi ṭuruq literature |
| `supplications-visitations` | Duʿaʾ collections, ziyara literature, mafatih al-jinan tradition |
| `poetry-collections` | Classical Arabic poetry: al-Mutanabbi, al-Maʿarri, qasaʾid traditions, didactic poetry |
| `contemporary-islamic-issues` | Modern works on contemporary issues |
| `journals-miscellaneous` | Periodicals, mixed collections |
| `bibliographies-indexes` | Bibliographic encyclopedias (Hajji Khalifa's Kashf al-Zunun, Aga Buzurg al-Tihrani's al-Dhariʿa) |
| `manuscripts` | Manuscript-studies materials (codicology, text-critical apparatus) |

Foundational source for `shards/tasawwuf.yaml`: **al-Qushayri, al-Risala
al-Qushayriyya** (sol_id `CB78uu0F`) — the canonical Sufi handbook
codifying maqamat and aḥwāl.

## Cross-domain edges

Most scholarly questions cross domain boundaries. The graph is designed
so a single query can traverse from a fiqh ruling, through the hadith
that grounds it, through the rijal of that hadith's chain, into the
tafsir works that engage with the same legal verse, into the kalam
positions that frame the controversy, and out to the history works that
contextualize the original ruling event. ADR 0004 (graph ontology)
specifies the cross-domain edge contracts.

## Implementation status by domain

As of 2026-05-03, the controlled vocabularies for each domain are
grounded in primary corpus works and committed to `config/shards/`:

| Domain | Vocabulary status | Lexicons (Arabic surface forms) |
|---|---|---|
| Hadith methodology | Settled (Nukhbat al-Fikr) | Pending — load when Phase 3 hadith extractor builds |
| Rijal grading | Settled (Sunni: Taqrib; Shia: Khulasat, Najashi) | **Settled** — `config/lexicons/rijal.yaml` |
| Qurʾanic sciences | Settled (al-Zarkashi's 47 anwāʿ) | Pending |
| Fiqh | Settled (al-Mustasfa, al-Risala, Mughniyya) | Pending |
| Kalam (cross-tradition) | Settled (al-Hilli, al-Taftazani) | Pending |
| Imamate (Shia-specific) | Settled (al-Mufid, al-Hilli) | Pending |
| Tasawwuf | Settled (al-Qushayri) | Pending |
| Linguistic disciplines | Settled (al-Tahanawi) | Pending |
| Philosophical disciplines | Settled (al-Tahanawi) | Pending |
| Natural sciences | Settled (al-Tahanawi) | Pending |
| Alignment axes (5) | Settled (Ibn Hajar's Taqrib rank-5) | Pending |
| Event types | Settled | Pending |
| Sira / sira-event types | Settled | Pending |
| Masumin canonical list | Settled (al-Mufid's al-Irshad) | Pending — seed data already structured |

"Pending" lexicons are added per-domain as Phase 3 (EXTRACT) extractors
for that domain come online (per the lexicon convention — see memory
`lexicon_convention.md` and ADR 0006).

## What this corpus is NOT

- It is not a Sunni-only or Shia-only corpus. Both traditions are
  represented across every applicable category, and the graph schema
  namespaces tradition-specific values (e.g., `THIQA` means different
  things in Sunni vs Shia rijal — both are first-class).
- It is not a hadith-only corpus, despite the conceptual richness of
  hadith methodology. Fiqh (12 categories), History+Biography (3
  categories totaling >3 GB of data), Linguistics (1.2 GB), and
  Ethics/Sufism (~830 MB) are all major surfaces.
- It is not modern: most works are pre-modern classical (3rd-13th
  century AH / 9th-19th century CE), with a `contemporary-islamic-issues`
  category for modern material.
- It is not in a single language: the corpus is overwhelmingly Arabic,
  with significant Persian content (especially in shia-theology and
  later philosophy categories).
