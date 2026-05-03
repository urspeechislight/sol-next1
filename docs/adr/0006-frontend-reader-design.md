# ADR 0006 — Frontend reader design

**Date:** 2026-05-02
**Status:** Proposed — do not implement until accepted

## Context

The frontend exists to let scholars browse and read the corpus. Sol's
predecessor reader (Remix + React) is feature-rich; sol-next1's reader
must do the same job in SvelteKit + Svelte 5 + Tailwind 4 *and* respect
the harness's strict SSOT rules (tokens.css, primitives, no inline
styles, no raw colors outside tokens.css).

This document specifies every decision needed before code is written:
information architecture, routes, page layouts, search architecture,
reader UX, state partitioning, theme model, component inventory, API
contracts, accessibility, empty/error/loading states, mobile responsive
behavior, and future extensibility points.

Where I am committing to a design choice, it appears under **Decision**.
Where I am proposing but the project owner must sign off, it appears
under **Open** at the end. Nothing in this document is implemented until
the owner reviews and the status changes to *Accepted*.

## Audience

The reader serves three user archetypes:

1. **Scholar** — reads classical texts in Arabic, may use English
   translation when available, uses TOC and chapter-level navigation,
   wants citation-stable URLs, cares about Arabic typography quality.
2. **Researcher** — searches across the corpus for a person, term, or
   topic; navigates from a result into a specific passage; may compare
   across books.
3. **Casual reader** — browses by category to discover books; reads
   selectively; relies on visual hierarchy more than search.

Every navigation decision below is justified against at least one of
these three.

## Information architecture

### Levels of navigation

Five distinct contexts; each gets its own affordance:

1. **Cross-corpus** — picking a category among 39 (or searching the
   whole corpus by title/author).
2. **In-category** — picking a book among the books in one category.
3. **Book-to-book** — moving between books at any time (always-available
   header).
4. **In-book** — moving between pages or chapters within a book.
5. **In-page** — scrolling within a page; jumping to footnotes; following
   in-text links (citations to other works, when Phase 5 ships).

### The 39 categories — domain grouping

39 is too many for a flat menu. The categories partition into 7
scholarly domains. **The grouping itself needs scholarly review (see
Open §1) — this is a starting proposal.**

| Domain | Categories | Count |
|---|---|---|
| Hadith | shia-hadith-fiqh, shia-hadith-general, shia-hadith-narrators, sunni-hadith-fiqh, sunni-hadith-general, sunni-hadith-narrators, fiqh-terminology | 7 |
| Qur'an Sciences | shia-tafsir, sunni-tafsir, quran-sciences | 3 |
| Fiqh (Jurisprudence) | hanafi-fiqh, hanbali-fiqh, maliki-fiqh, shafii-fiqh, zahiri-fiqh, zaidi-fiqh, shia-fiqh-{8th-century, fatwas, pre-8th-century, principles}, sunni-fiqh-principles, independent-fiqh | 12 |
| Theology & Sects | shia-theology, sunni-theology, sects-schools | 3 |
| Biography & History | genealogy-biography, prophet-imams-biography, history-geography | 3 |
| Sciences | arabic-language-sciences, logic-philosophy, medicine, other-sciences | 4 |
| Devotional & Other | ethics-mysticism, supplications-visitations, poetry-collections, contemporary-islamic-issues, journals-miscellaneous, bibliographies-indexes, manuscripts | 7 |

The grouping is encoded in `src/frontend/lib/category-domains.ts`
(read-only; ordering matters for display). It's data, not configuration
— changes to this grouping go through a code review, not a YAML edit.

### Sitemap

```
/                                       (home — categories grouped by domain)
/library/[category]                     (books in a category)
/search?q=...                           (global search results)
/read/[urn]?p=N                         (reader, page N)
/read/[urn]?p=N&q=...                   (reader with in-book search panel)
/read/[urn]?p=N&toc=1                   (reader with TOC pinned open)

/about                                  (deferred; see Open §6)
/healthz, /readyz                       (already exist; backend only)
```

**No book-detail intermediate page.** The book card surfaces all
metadata (title AR/EN, author, death year, page count, sectarian tag,
canonical_status). Clicking goes directly to `/read/[urn]?p=1`. Sol's
pattern. Justification: a separate detail page adds a click between
discovery and reading without surfacing information the card already
shows. (See Open §2 — the project owner may want to override.)

## URL structure

**URL state is the navigation truth.** Sharing a URL must reproduce the
view exactly. Settings (theme, font size, language preference) are
per-user and live in localStorage, *not* in the URL.

| State | Lives in | Why |
|---|---|---|
| Current category | URL path (`/library/[category]`) | Shareable, refresh-safe |
| Current book | URL path (`/read/[urn]`) | Shareable; URN is the stable handle (sol_id) |
| Current page | URL query (`?p=15`) | Citation-stable; browser back works |
| In-book search query | URL query (`?q=...`) | Shareable; reproducible search state |
| TOC open/closed | URL query (`?toc=1`) | Shareable view; default closed on mobile, open on desktop unless overridden |
| Library sort/filter | URL query | Shareable; library is a stateful surface |
| Reader theme | localStorage | Per-user preference; doesn't survive across users sharing a link |
| Reader font size | localStorage | Same |
| Language mode (AR/EN/AR\|EN) | localStorage | Same |
| Reader line-height | localStorage | Same |

**Key:** `urn` in the URL is the book's `sol_id` (alphanumeric, e.g.
`OXlyzwsl`), not the numeric `book_id`. Stable across reformatting and
matches the corpus's stable handle.

## Page layouts

ASCII shape only — actual visual design follows the existing design
system (tokens, primitives). Spacing/typography come from `tokens.css`.

### `/` — Home (categories grouped by domain)

```
┌──────────────────────────────────────────────────────────────────────────┐
│ AppHeader                                                                │
├──────────────────────────────────────────────────────────────────────────┤
│ Hadith                                                                7  │
│   ┌────────┐ ┌────────┐ ┌────────┐ ... 7 cards ...                       │
│   │shia-   │ │shia-   │ │shia-   │                                      │
│   │hadith- │ │hadith- │ │hadith- │                                      │
│   │ fiqh   │ │general │ │narrato │                                      │
│   │ 12     │ │ 8      │ │ 24     │                                      │
│   └────────┘ └────────┘ └────────┘                                       │
│                                                                          │
│ Qur'an Sciences                                                       3  │
│   ┌────────┐ ┌────────┐ ┌────────┐                                       │
│   │ shia-  │ │ sunni- │ │ quran- │                                       │
│   │ tafsir │ │ tafsir │ │ sci    │                                       │
│   └────────┘ └────────┘ └────────┘                                       │
│                                                                          │
│ ... 5 more domain groups ...                                             │
└──────────────────────────────────────────────────────────────────────────┘
```

- Each `CategoryCard` shows: category slug (humanized), Arabic label
  (when applicable), and book count.
- Cards click through to `/library/[category]`.
- Group headers are scoped headings for screen readers.

### `/library/[category]` — Books in a category

```
┌──────────────────────────────────────────────────────────────────────────┐
│ AppHeader                                                                │
├──────────────────────────────────────────────────────────────────────────┤
│ ← Hadith                                              Shia Hadith        │
│   مصادر رجال الحديث عند الشيعة                          24 books         │
│ ──────────────────────────────────────────────────────────────────────── │
│   [ 🔍 Search in this category... ]      [ Sort: Author ▾ ]  [Filter ▾]  │
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │ كتاب الرجال                              Al-Najashi              │   │
│   │ Rijal al-Najashi                         d. 450 AH               │   │
│   │                                          624 pages • Imami       │   │
│   │                                          primary source          │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │ ...                                                              │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│   [Pagination — load more]                                               │
└──────────────────────────────────────────────────────────────────────────┘
```

**In-category search** is a separate input from the corpus search in
the header. Scope is the category only. Matches title_ar / title_en /
author / author_en. Live-filters the visible book list (no server
round-trip if the category has < 200 books — a single fetch loads
all, then JS filters).

**Sort options:** Title (Arabic alpha), Author (alpha), Death year (ascending),
Page count (descending), Canonical status (primary first).

**Filters:**
- Sectarian affiliation (sunni / shia / other)
- Madhab (when applicable)
- Language (Arabic / Persian / mixed)
- Canonical status (primary / secondary / all)
- Author lifetime range (e.g., 1st-3rd century AH, 4th-7th, 8th-12th, modern)

Filters are URL-state (queryparams). Multiple selections combine AND.

### `/search?q=...` — Global search results

```
┌──────────────────────────────────────────────────────────────────────────┐
│ AppHeader                                                                │
├──────────────────────────────────────────────────────────────────────────┤
│ Search results for "ibn hajar"                              46 results   │
│ ──────────────────────────────────────────────────────────────────────── │
│                                                                          │
│ Sunni Hadith — Narrators                                       12 books  │
│   ┌──────────────────────────────────────────────────────────────────┐   │
│   │ تقريب التهذيب                            Ibn Hajar al-Asqalani   │   │
│   │ Taqrib al-Tahdhib                        d. 852 AH               │   │
│   │ Pages: 1-777                                                     │   │
│   └──────────────────────────────────────────────────────────────────┘   │
│   ... more cards ...                                                     │
│                                                                          │
│ Sunni Hadith — General                                          8 books  │
│   ... more cards ...                                                     │
│                                                                          │
│ ... grouped by category ...                                              │
└──────────────────────────────────────────────────────────────────────────┘
```

**v1 search scope:** title_ar, title_en, author, author_en across all
books. Substring after Arabic normalization (using the same
`normalize_arabic` we built for lexicons). Returns books grouped by
category.

**Phase-5 search scope (deferred):** full-text content via Postgres
FTS + Neo4j vector hybrid (per ADR 0003). Same UI; richer results with
passage snippets.

### `/read/[urn]?p=N` — Reader

The reader is a *full-screen takeover*. AppHeader is replaced by
ReaderToolbar. There's no global navigation visible inside the reader
— a deliberate UX choice for reading focus, modeled on sol.

```
┌─ ReaderToolbar ─────────────────────────────────────────────────────────────┐
│ [← Library]  كتاب الرجال • Al-Najashi                                       │
│              ────────────────────────────────────                           │
│              [‹ Prev chapter] [‹ Page] [13/624 ↡] [Page ›] [Next chapter ›] │
│              ────────────────────────────────────                           │
│              [Bright | Dark | Classical]   [Aa-  Aa+]                       │
│              [AR | EN | AR|EN]   [⌘F Search]   [☰ TOC]                      │
└─────────────────────────────────────────────────────────────────────────────┘
┌─ ReaderTOC (sidebar — collapsible) ──┐ ┌─ Reader content area ──────────────┐
│ Contents                              │ │  [Arabic body, dir=rtl,            │
│ • Introduction                  p 3   │ │   font-arabic, reader theme]      │
│ ▸ Chapter 1: Names ا            p 11  │ │                                    │
│ • Chapter 2: Names ب            p 109 │ │  Page 13 ────────────              │
│ • ...                                  │ │                                    │
│ • Indices                       p 567 │ │  [more text]                      │
│                                       │ │                                    │
│ ─────                                 │ │                                    │
│ [‹ Prev chapter] [Next chapter ›]     │ │                                    │
└───────────────────────────────────────┘ └────────────────────────────────────┘
                                          ┌─ Progress bar ─────────────────────┐
                                          │ ▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░  │
                                          └────────────────────────────────────┘
```

#### Toolbar — three rows

The toolbar packs a lot of controls. Three rows is more readable than
one busy strip:

**Row 1 — context:** back link, book title (AR + EN), book author. The
"back" link goes to `/library/[category]` for the book's category. The
title is informational only; it's the toolbar header, not a link.

**Row 2 — pagination:** prev-chapter, prev-page, page indicator pill
(shows `13 / 624`), next-page, next-chapter. The pill is clickable —
opens an inline mini-input to type a page number; Enter jumps to that
page. ESC cancels.

**Row 3 — settings + tools:** theme switcher, font size +/-, language
mode (AR / EN / AR|EN), search-in-book button, TOC toggle.

#### Mobile toolbar collapsing

On mobile (< 768px), the toolbar collapses:

```
┌─ ReaderToolbar (mobile) ────────────────────────────────────┐
│ [←]  كتاب الرجال                  [13/624]  [☰]  [⋯ More]   │
└─────────────────────────────────────────────────────────────┘
```

- "←" goes back to library
- Title truncates with ellipsis
- Page pill is still there (tappable for jump)
- ☰ opens TOC drawer (right-aligned, RTL-aware)
- ⋯ opens an overflow menu with: Theme / Font size / Language mode /
  Search in book

The pagination chevrons (prev/next page, prev/next chapter) become
swipe gestures on mobile (left-swipe = next page in LTR; in RTL Arabic
content, right-swipe = next page).

#### TOC

- **Desktop:** Sidebar (left for LTR layout, right for RTL); 320px
  wide; pinned by default. URL `?toc=0` collapses it.
- **Mobile:** Drawer (right side for RTL — slides in from the side
  toward which Arabic text reads). Overlay backdrop. Closed by default.
- **Active entry:** highlighted via IntersectionObserver tracking
  visible page anchors (sol's `useTocSync` pattern).
- **TOC entries:** title + page number; clicking either jumps to that
  page (modifies URL `?p=`).
- **No TOC available:** if `book.toc` is empty, the TOC button is
  disabled with tooltip "No table of contents."
- **Long TOCs:** if more than 50 entries, show a "Filter…" input above
  the list.

#### Pagination

- **Page-level:** prev-page / next-page buttons → `?p=N±1`.
- **Chapter-level:** prev-chapter / next-chapter → jump to the prev /
  next TOC entry's page_number. If at the last chapter, next is
  disabled.
- **Direct jump:** click the `13/624` pill → inline number input.
- **Keyboard:** `←` and `→` arrows move pages; `Shift+←` / `Shift+→`
  move chapters; `g` then page number jumps directly (vim-style; needs
  explicit opt-in indicator).

#### Reader settings

Live in localStorage under `sol-reader-settings` (single JSON object).
Hydrated on mount; persisted on change.

```ts
interface ReaderSettings {
  theme: 'bright' | 'dark' | 'classical';
  fontSize: 14 | 16 | 18 | 20 | 22 | 24;       // px scale
  lineHeight: 'compact' | 'normal' | 'relaxed';  // → 1.4 / 1.7 / 2.0
  langMode: 'ar' | 'en' | 'both';
  fontFamily: 'scheherazade' | 'amiri';          // Arabic typeface
}

const DEFAULT_SETTINGS: ReaderSettings = {
  theme: 'classical',           // sepia is most pleasant for long Arabic reads
  fontSize: 20,
  lineHeight: 'normal',
  langMode: 'ar',
  fontFamily: 'scheherazade',
};
```

When the user requests `langMode: 'en'` but the book has no English,
the toolbar shows the toggle disabled with explanation; PageView
renders the `TranslationPlaceholder` composed component.

#### Translation placeholder (Phase 4 forward-compat)

API returns `{text_ar: string, text_en: string | null, footnote_ar?: ..., footnote_en?: ...}`.

`PageView` rendering rules:
- `langMode='ar'`: render `text_ar` only.
- `langMode='en'` and `text_en` is non-null: render English only.
- `langMode='en'` and `text_en` is null: render `TranslationPlaceholder`
  with body "Translation not yet available for this book."
- `langMode='both'` and `text_en` is non-null: side-by-side grid
  (Arabic right column, English left column for visual balance with
  RTL/LTR meeting at the gutter).
- `langMode='both'` and `text_en` is null: Arabic full-width,
  `TranslationPlaceholder` underneath ("Translation pending — when
  available it will appear here").

When Phase 4 (ENRICH) ships, `text_en` becomes non-null for translated
books. **Zero frontend changes required.**

#### In-book search

- Triggered by toolbar button or `⌘F` keyboard shortcut (preventDefault
  on browser's native Find, since browser Find can't see virtualized
  page content).
- Opens a panel that *replaces* the TOC sidebar (same width, same
  position). Sidebar mode is a single slot.
- Backend endpoint: `GET /api/books/{urn}/search?q=...&limit=N`.
- Backend uses `normalize_arabic` from `pipeline.utils.arabic` to
  normalize both query and page text before substring match (the first
  consumer of the normalizer outside lexicons).
- Result list: `[{page_number, snippet, match_count}]` — snippet shows
  ~80 characters around the match, with the matched substring marked.
- Clicking a result jumps to that page; the matched substring is
  highlighted in the rendered page (via a `<mark>` element wrapped by
  the `ArabicProse` primitive when its `highlight` prop is set).
- Search query is URL-state (`?q=`), so refresh restores the search.

#### Scroll behavior

**Single-page-at-a-time, not auto-pagination.**
- Each route render shows exactly one page (`?p=N`).
- Prev/Next buttons trigger SvelteKit navigation; URL updates; new page
  fetches.
- Sol's auto-pagination on scroll is *removed* in our design. Reasons:
  - Citation stability (the page in the URL is always the page on
    screen)
  - Predictable backend load (one request per navigation, not on every
    scroll event)
  - Better screen-reader behavior (the page heading is announced once)
- Mobile: swipe left/right between pages; respects RTL on Arabic
  content.

If we discover users want continuous scroll, it can be added later as
an opt-in setting (`?scroll=continuous`).

#### Progress bar

A thin horizontal bar at the bottom of the reader content area showing
*book-level* progress: `(current_page / total_pages) × 100%`. It does
*not* show in-page scroll progress (we don't auto-paginate; in-page
scroll is just scroll).

#### Themes

Three reader themes; full color palettes are in `tokens.css` under
`[data-reader-theme="..."]` selectors. The reader root element gets
`data-reader-theme={settings.theme}`. All reader components consume
`var(--color-reader-*)` tokens via Tailwind classes.

| Theme | Surface | Text | Vibe |
|---|---|---|---|
| `bright` | #FFFFFF | #1A1A1A | clean, high-contrast, daytime |
| `dark` | #121212 | #E8E8E8 | low-light reading |
| `classical` | sepia (#FDFBF7) | warm brown (#3D3024) | extended Arabic reading; **default** |

Color values illustrative; final values come from `tokens.css` after
review.

**Reader themes are independent of app theme.** The app shell
(AppHeader, library pages, search) uses light/dark via the existing
`[data-theme=...]` mechanism. The reader has its own three-theme axis
because reading typography deserves dedicated treatment. The reader's
3 themes don't affect the app shell; the app's light/dark doesn't
affect the reader.

#### Footnotes (deferred to Phase 2)

Phase 1 stores `Page.footnote_text` as raw text. Phase 2 (SEGMENT)
will identify in-text footnote markers and parse the `footnote_text`
into structured `[{number, text}]` entries.

For now, the reader displays footnote text as a separate paragraph
beneath each page's body, headed "Footnotes". No popovers — those
require parsed marker positions that don't exist yet. When Phase 2
ships, the existing display becomes interactive popovers (added in a
follow-up).

#### Accessibility

- **RTL primary direction** for Arabic content; LTR for chrome.
- `dir="rtl"` on `<ArabicProse>` instances; `dir="ltr"` on chrome.
- Mixed-content blocks (book card with English label + Arabic title)
  use Unicode bidi neutrally; no manual `&rlm;` insertion.
- All toolbar buttons have `aria-label` (e.g., "Previous page",
  "Toggle table of contents").
- TOC entries are `<a>` elements (keyboard-navigable, focusable).
- Page numbers are read aloud as `"Page 13 of 624"`.
- Skip-to-content link at the top of the reader (focusable, hidden
  visually).
- Heading hierarchy: AppHeader is `<header role="banner">`, page
  body has `<main>`, ReaderToolbar is `<header>` *inside* the reader's
  `<main>` (the reader is the page's main content).
- Color contrast: every reader theme meets WCAG AA (4.5:1 for body
  text, 3:1 for large text). Validated as part of the tokens.css
  review.
- Reduced motion: existing `tokens.css` already honors
  `prefers-reduced-motion` — page transitions disable.

## Three-tier search architecture

| Tier | Where the input lives | Scope | Backend endpoint | Returns |
|---|---|---|---|---|
| Corpus | AppHeader (always visible) | All books across all categories | `GET /api/search?q=...&limit=...` | Books grouped by category |
| Category | `/library/[category]` toolbar | Books in one category | none — client-side filter | Filtered visible book list |
| Book | Reader toolbar (`⌘F`) | Pages within one book | `GET /api/books/{urn}/search?q=...` | Pages with snippets |

Three because the user genuinely needs three different scopes; one
search field handling all of them is confusing. The visual treatment
(input shape, icon, placeholder) is consistent across the three but
each lives in a different layout context.

**All three** use `normalize_arabic` server-side (and where applicable
client-side for category filtering) so the user can type with or
without diacritics, with or without the definite article, and find
matches.

## Component inventory

Strictly partitioned per the harness's SSOT rules.

### `lib/design-system/tokens.css` — design tokens (only place colors live)

New additions:
- `--font-arabic: 'Scheherazade New', 'Amiri', serif`
- `--font-arabic-display: 'Amiri', 'Scheherazade New', serif` (titles)
- `--text-reader-{xs,sm,base,lg,xl,2xl}` — px scale 14, 16, 18, 20, 22, 24
- `--leading-reader-{compact,normal,relaxed}` — 1.4, 1.7, 2.0
- 3 reader-theme variable groups under `[data-reader-theme="..."]`
  selectors: `--color-reader-{bg,fg,muted,border,toolbar-bg,toolbar-fg,
  pill-bg,pill-fg,quote-bg,honorific,progress,popover-bg,popover-border,
  match-highlight}` × 3 themes ≈ 36 new tokens.

### `lib/design-system/tokens.ts` — TypeScript-side mirror

Add token name constants for the new entries above so TS code can
reference them by name (existing convention).

### `lib/design-system/variants.ts` — variant maps

Add (if needed):
- `langModeVariants` — display/grid setup per `langMode`
- `bookCardVariants` — sectarian-affiliation badge color
- `categoryCardVariants` — domain-group accent color
- `themeSwatchVariants` — appearance per reader theme name

### `lib/design-system/primitives/`

| File | Purpose | Status |
|---|---|---|
| Button.svelte | Existing | — |
| Badge.svelte | Existing | — |
| Card.svelte | Existing | — |
| Input.svelte | Existing | — |
| Stack.svelte | Existing | — |
| Text.svelte | Existing | — |
| Icon.svelte | Existing | — |
| **Link.svelte** | **NEW** — wraps `<a>` for SvelteKit nav; required because routes can't use raw `<a>` | New |
| **ArabicProse.svelte** | **NEW** — RTL Arabic body text; uses `--font-arabic`, reader sizes, reader line-heights; accepts `text` and optional `highlight` prop for in-book search | New |
| **EnglishProse.svelte** | **NEW** — LTR English body text (mirror of above) | New |
| **MenuButton.svelte** | **NEW** — header dropdown trigger (for Browse menu) | New |
| **SegmentedControl.svelte** | **NEW** — used for theme switcher and lang mode toggle | New |

### `lib/design-system/composed/`

All reader-specific UI.

| File | Composes | Used in |
|---|---|---|
| HealthBadge.svelte | Existing | (existing) |
| **AppHeader.svelte** | Logo (Text), MenuButton, Input (search), Button (theme) | Root layout (non-reader) |
| **BrowseMenu.svelte** | List of CategoryCards grouped by domain | AppHeader dropdown |
| **CategoryCard.svelte** | Card, Text, Badge | Home, BrowseMenu |
| **BookCard.svelte** | Card, Text, Badge, Stack | Library page, search results |
| **ReaderToolbar.svelte** | Button, Link, Input, SegmentedControl | Reader |
| **ReaderTOC.svelte** | Link, Input (filter), Button | Reader |
| **PageView.svelte** | ArabicProse, EnglishProse, TranslationPlaceholder | Reader |
| **PageSeparator.svelte** | Text | Reader (between pages) |
| **ProgressBar.svelte** | (none — pure markup with CSS) | Reader |
| **TranslationPlaceholder.svelte** | Text, Icon | PageView |
| **PageJumpInput.svelte** | Input | ReaderToolbar (inline jump-to-page) |
| **InBookSearchPanel.svelte** | Input, Link (per result) | Reader (replaces TOC slot) |

### `lib/stores/` — Svelte 5 rune-based stores

| File | Purpose |
|---|---|
| theme.ts | Existing (app theme) |
| **reader-settings.ts** | Reader settings (3 themes, font size, line height, langMode, fontFamily); localStorage-persisted |

### `lib/server/` — server-side only

| File | Purpose |
|---|---|
| api-client.ts | Existing |
| **library.ts** | Typed wrappers around backend library endpoints |

### `lib/category-domains.ts` — pure data

Maps the 39 categories to 7 domain groups. Read by AppHeader's
BrowseMenu and by `/` (home page).

### Routes

Thin orchestration only — no logic beyond data wiring.

| Route file | Purpose |
|---|---|
| `routes/+layout.svelte` | Root layout: `<AppHeader />` + `<slot />` |
| `routes/+layout.server.ts` | (existing) |
| `routes/+page.svelte` | Home — composes `<CategoryCard>` × 39 grouped by domain |
| `routes/library/[category]/+page.svelte` | Category page — composes `<BookCard>` × N |
| `routes/library/[category]/+page.server.ts` | Loader: fetch books in category |
| `routes/search/+page.svelte` | Search results — composes `<BookCard>` grouped by category |
| `routes/search/+page.server.ts` | Loader: call backend `/api/search?q=` |
| `routes/read/[urn]/+layout.svelte` | Reader layout (overrides root layout's AppHeader) — mounts `<ReaderToolbar>` instead |
| `routes/read/[urn]/+page.svelte` | Reader page — composes `<PageView>` + `<ReaderTOC>` + `<ProgressBar>` |
| `routes/read/[urn]/+page.server.ts` | Loader: fetch book metadata, TOC, page N |

## API contracts

All backend endpoints under `/api/`. Filesystem-backed initially (reads
JSON from `data/books/`); will move to Postgres-backed when persistence
ships.

| Method | URL | Returns | Errors |
|---|---|---|---|
| GET | `/api/categories` | `{categories: [{slug, label_ar, label_en, book_count}]}` | — |
| GET | `/api/categories/[slug]` | `{slug, label_ar, label_en, book_count, books: [BookSummary]}` | 404 if unknown slug |
| GET | `/api/books/[urn]` | `BookDetail` (frontmatter + toc + page_count, no content) | 404 if unknown urn |
| GET | `/api/books/[urn]/pages/[n]` | `Page` `{page_number, text_ar, text_en \| null, footnote_ar, footnote_en \| null}` | 404 if unknown urn or page |
| GET | `/api/books/[urn]/search?q=...&limit=20` | `{matches: [{page_number, snippet, match_count}], total}` | 400 if q missing |
| GET | `/api/search?q=...&limit=50` | `{books: [BookSummary grouped by category], total}` | 400 if q missing |

### Data shapes

```ts
interface BookSummary {
  urn: string;             // sol_id
  title_ar: string;
  title_en: string | null;
  author: string;
  author_en: string | null;
  death_year_ah: number | null;
  page_count: number;
  category: string;
  sectarian_affiliation: string | null;
  madhab: string | null;
  canonical_status: 'primary' | 'secondary';
  language: string;
}

interface BookDetail extends BookSummary {
  toc: TocEntry[];
}

interface TocEntry {
  page_number: number;
  title: string;
  title_en?: string | null;
}

interface Page {
  page_number: number;
  text_ar: string;
  text_en: string | null;          // null until Phase 4 (ENRICH)
  footnote_ar: string | null;
  footnote_en: string | null;
}
```

### CORS / auth

- v1: anonymous, no auth, public read-only.
- CORS allows the frontend origin from `SOL_CORS_ORIGINS` env var
  (already configured in `.env.example`).

## Empty / error / loading states

For every route, the explicit handling:

| State | Behavior |
|---|---|
| Home — no categories (corpus empty) | "No content available — pipeline not yet run." with link to docs/contributing.md |
| Library — empty category | "No books in this category yet." |
| Library — invalid category slug | 404 page → "Category not found" + link to home |
| Search — no results | "No books match \"{q}\". Try {suggestion}." with empty-state illustration |
| Reader — invalid URN | 404 page → "Book not found" |
| Reader — page out of range | redirect to nearest valid page (`?p=clamp(p, 1, page_count)`) |
| Reader — TOC missing | TOC button disabled with tooltip; sidebar shows empty-state with "This book has no table of contents" |
| Reader — page text empty | "This page has no content" with "← Previous page" link |
| Reader — translation requested but unavailable | TranslationPlaceholder component (per §reader UX above) |
| In-book search — no results | "No matches for \"{q}\" in this book." |
| In-book search — query too short | "Type at least 2 characters." |
| Backend offline | App-level error boundary: "Backend unavailable. Try again in a moment." with retry button |
| Slow load (> 500ms) | Skeleton loader (Card-shaped placeholders for grid views; text-shaped for reader) |
| Hard navigation between pages | Page-transition spinner only if request takes > 200ms (else seamless) |

## Mobile responsive plan

Breakpoints (matching Tailwind defaults):
- `sm` 640px — phone landscape, small tablet portrait
- `md` 768px — tablet
- `lg` 1024px — small laptop
- `xl` 1280px — desktop

Per-route behavior:

| Route | < md | ≥ md |
|---|---|---|
| Home | Single-column stacked groups | Multi-column grid per group |
| Library | Single-column book cards | Two-column book cards |
| Search results | Single-column | Single-column (results are full-width per category section) |
| Reader | Toolbar collapses to 3-button bar; TOC is drawer; pagination via swipe + tap pill | Full toolbar (3 rows); TOC sidebar pinned; chevrons + pill |

## Future extensibility points

Built into the design now so they slot in without rework:

| Future | Hook in this design |
|---|---|
| Phase 4 translations | `Page.text_en` is already `string \| null`; reader renders or shows placeholder per current value. No frontend changes needed. |
| Phase 5 full-text search | Same `/api/search` endpoint; backend swaps from substring-on-frontmatter to PostgresFTS / Neo4j vector hybrid. Same response shape. |
| Phase 5 graph queries | New page type `routes/graph/[urn]` for entity exploration; deferred to a follow-up ADR. |
| Bookmarks / reading progress | Future `lib/stores/bookmarks.ts`; per-book stored in localStorage; sync layer if accounts ship. |
| User accounts | Future `routes/account/`; SSO or magic-link; until then everything is anonymous. |
| Citations & sharing | Future right-click on a paragraph → "Cite this passage" → copies a URL with `?p=N&para=M` and a formatted reference. |
| Footnote popovers | When Phase 2 (SEGMENT) ships parsed footnote markers, the reader's footnote rendering switches from "list under page" to "click marker → popover" without redesign. |
| In-text citation linking | When Phase 5 (GRAPH) ships citation edges, in-text citations become hyperlinks to the cited work — uses the existing Link primitive. |
| Bilingual side-by-side | Already designed (langMode='both'); activates the moment any book has `text_en !== null`. |
| Other languages (Persian, Urdu) | `Page` model adds `text_fa`, `text_ur` etc.; reader settings adds new langMode values; PageView grows another conditional. The architecture absorbs this without restructuring. |

## What we are NOT building (v1 scope guard)

- Bookmarks, reading progress, user accounts (defer to future)
- Auto-pagination on scroll (deliberate choice — see §reader UX)
- Footnote popovers (need Phase 2 markers)
- Specialized rich-segment rendering (HonorificSegment, IsnadSegment,
  etc.) — need Phase 2/3 parsed units
- Bilingual side-by-side functional content (no text_en data exists;
  the *placeholder UI* exists)
- Citation export, share-passage UI
- In-text citation hyperlinks (need Phase 5)
- Print / PDF export
- Search history / saved searches
- Advanced filter combinators (boolean queries, regex)

These are explicitly out of v1 to keep the scope shippable. Each is
documented as an extensibility point above so we don't paint ourselves
into a corner.

## Open — decisions awaiting project owner sign-off

1. **Domain grouping of 39 categories** — see §IA. Specifically:
   - Should `fiqh-terminology` be in Hadith (which is what I proposed)
     or in Fiqh? Or its own group "Reference"?
   - Should `bibliographies-indexes` and `manuscripts` be a separate
     "Bibliographic" group, or remain in "Devotional & Other"?
   - Should `arabic-language-sciences` be its own "Linguistics" group
     given the corpus mass (~1.2 GB)?
2. **Direct-to-reader vs book-detail intermediate page** — I proposed
   direct (sol's pattern). If a book-detail page is wanted, add
   `/library/[category]/[urn]` route with metadata + "Open Reader"
   button.
3. **Default reader theme** — I proposed `classical` (sepia, gentlest
   for long Arabic reading). Override?
4. **Default Arabic font** — I proposed Scheherazade New (designed
   for Quranic typography; better tashkīl handling). Alternatives:
   Amiri (more ornamental, slower to render), Noto Naskh Arabic
   (Google), system stack only. **Practical question: do we self-host
   the font or load from Google Fonts?** Self-host = no third-party
   dependency, slower first paint; CDN = faster, dependency on Google.
5. **Continuous scroll vs single-page-per-route** — I proposed
   single-page (better for citation, predictable load). Sol does
   continuous + auto-pagination. Push back if you want continuous.
6. **`/about` and other static pages** — defer entirely or include in
   v1?
7. **Auth** — I propose anonymous in v1. Confirm?
8. **Mobile-first or desktop-first design priority?** — I treated them
   as equally important. If a priority is needed for ambiguous
   tradeoffs, which takes precedence?
9. **`⌘F` keyboard shortcut** — overrides browser's native Find. I
   propose yes (search the book content, not just visible DOM). Some
   users dislike apps that hijack `⌘F`. Alternatives: own button only,
   or shortcut `/`.
10. **Toolbar features** — anything missing? Specifically:
    - Bookmark current page?
    - Citation export (copy formatted reference)?
    - Reset settings to defaults?
    - "About this book" expansion (full frontmatter modal)?

## Decision (pending acceptance)

Approve everything in this document except the **Open** section,
which the project owner addresses inline. Once Open is resolved, the
status flips to `Accepted` and code begins along the
component-inventory order:

1. Tokens (CSS + TS)
2. New primitives (Link, ArabicProse, EnglishProse, SegmentedControl,
   MenuButton)
3. Backend library service + router (filesystem-backed)
4. Reader settings store
5. Composed components (in dependency order: BookCard, CategoryCard
   first; AppHeader and BrowseMenu next; PageView, ReaderTOC,
   ReaderToolbar last)
6. Routes (Home → Library → Search → Reader)
7. e2e Playwright spec covering: home → category → book → page →
   in-book search

## Consequences

**Positive**

- Every navigation context has its own affordance — no overloaded
  controls.
- URL state is the navigation truth; sharing a URL reproduces the view.
- Three-tier search has clear, distinct scopes.
- Reader is a focused, full-screen takeover — modeled on sol's working
  pattern.
- Translation placeholder means Phase 4 lights up the reader without
  frontend rework.
- Component inventory respects the harness's SSOT rules (tokens,
  primitives, composed, routes).
- Mobile is designed alongside desktop, not bolted on.

**Negative**

- The reader toolbar has many controls. A 3-row layout reduces clutter
  but requires more vertical space than sol's single-row toolbar.
- Three reader themes plus app light/dark = 6 effective combinations.
  Each needs design review for contrast (especially classical + dark
  app shell).
- Single-page-per-route loses sol's continuous scroll. Some users
  prefer continuous; reverting requires URL-state changes.
- The Arabic search-in-book endpoint runs Arabic normalization on
  every page of every book per query. Cache misses are worst-case
  ~5 MB of text per search. Acceptable until Phase 5 indexed search.
- Adding a Link primitive (because routes can't use raw `<a>`) adds
  one indirection layer for every link in the app. Acceptable cost
  of harness discipline.

## Alternatives considered

**Sol's auto-pagination on scroll.** Rejected for v1 — citation
stability matters more than the sensation of continuous reading at
this scale. Re-add as opt-in setting if user feedback warrants.

**Inline-style theming (sol's pattern).** Rejected — violates SSOT.
CSS custom properties + `data-reader-theme` does the same job in pure
CSS.

**One unified search field.** Rejected — three different scopes
(corpus / category / book) deserve three affordances. Conflating them
in one field hides the scope from users.

**Book-detail intermediate page.** Considered. Rejected by default
(see Open §2) — the BookCard already shows enough metadata; an extra
click adds friction without surfacing new info. Reversible if the
project owner wants it.

**Hash-fragment URLs (`#p=15`) instead of query (`?p=15`).** Rejected
— query params survive server-side rendering and are normal URLs.
Hash fragments are client-only.

## References

- ADR 0003 — storage stack
- ADR 0004 — graph ontology (translation lives at Unit level, not Page,
  per Phase 4)
- ADR 0005 — phase contracts (Phase 4 is the only writer of
  translations)
- `docs/foundation.md` — the data-integrity stance
- `docs/design-system.md` — design tokens, primitives, variants
- Memory: `data_layout.md` — corpus JSON shape (frontmatter / toc /
  content)
- Sol's reader: `~/code/sol/apps/web/app/components/reader/`
  (Remix + React; reference patterns, not a target for code-copying —
  the standalone contract holds)
