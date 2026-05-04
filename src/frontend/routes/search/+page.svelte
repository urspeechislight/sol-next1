<!--
  Search — cross-corpus results. Layout: results column on the left
  (narrators, passages, books grouped by category), scope facets sidebar
  on the right. Reads ?q= from the URL; live-updates as the user types.
-->
<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { Breadcrumb, Input, Pressable, BookCard } from '$lib/design-system';
  import { BOOKS, DOMAINS } from '$lib/fixtures';
  import SearchScope from '$lib/components/search/SearchScope.svelte';

  const initialQ = $derived(String(page.url.searchParams.get('q') ?? ''));
  let q = $state('');

  // Sync local input from URL when it changes (eg back/forward).
  $effect(() => {
    q = initialQ;
  });

  function commit(value: string) {
    void goto(`/search?q=${encodeURIComponent(value)}`, { keepFocus: true, noScroll: true });
  }

  function onKey(e: KeyboardEvent) {
    if (e.key === 'Enter') commit(q.trim());
  }

  const ql = $derived(q.toLowerCase().trim());

  const matches = $derived.by(() => {
    if (!ql) return BOOKS;
    return BOOKS.filter((b) =>
      [b.titleAr, b.titleEn, b.author, b.authorAr]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(ql),
    );
  });

  const passageHits = $derived.by(() => {
    if (!ql) return [];
    return [
      {
        bookAr: 'الكافي',
        bookEn: 'al-Kafi',
        urn: 'KafSlm32',
        page: 109,
        snippetAr:
          'رَأَتْهُ الْقُلُوبُ بِنُورِ الْإِيمَانِ، وَأَثْبَتَتْهُ الْعُقُولُ بِيَقَظَتِهَا...',
        snippetEn: 'Hearts have seen Him by the light of faith…',
      },
      {
        bookAr: 'فتح الباري',
        bookEn: 'Fath al-Bari',
        urn: 'FathBari',
        page: 482,
        snippetAr: 'وَقَدْ رَوَى هَذَا الْحَدِيثَ ابْنُ حَجَرٍ بِإِسْنَادٍ آخَرَ...',
        snippetEn: 'Ibn Hajar transmits this hadith with a different chain…',
      },
    ];
  });

  const narratorHits = $derived.by(() => {
    if (!ql) return [];
    if (!ql.includes('hisham') && !ql.includes('ibn')) return [];
    return [
      {
        name: 'Hisham ibn al-Hakam',
        nameAr: 'هشام بن الحكم',
        d: 199,
        role: 'Mutakallim, companion of al-Sadiq',
        count: 1247,
      },
      {
        name: 'Hisham ibn Salim al-Jawaliqi',
        nameAr: 'هشام بن سالم الجواليقي',
        d: 179,
        role: 'Companion of al-Sadiq',
        count: 612,
      },
    ];
  });

  const grouped = $derived.by(() => {
    const out: Record<string, typeof BOOKS> = {};
    for (const b of matches) {
      const arr = out[b.category] ?? [];
      arr.push(b);
      out[b.category] = arr;
    }
    return Object.entries(out);
  });

  function findCat(slug: string) {
    for (const d of DOMAINS) {
      for (const c of d.categories) {
        if (c.slug === slug) return { ...c, domain: d };
      }
    }
    return null;
  }

  const sectImami = $derived(matches.filter((b) => b.sect === 'imami').length);
  const sectSunni = $derived(matches.filter((b) => b.sect === 'sunni').length);
  const primary = $derived(matches.filter((b) => b.canonical === 'primary').length);
</script>

<svelte:head>
  <title>{ql ? `Search: ${q}` : 'Search'} · Shia Online Library</title>
</svelte:head>

<div class="search">
  <Breadcrumb items={[{ label: 'Browse', href: '/' }, { label: 'Search' }]} />

  <header class="search__head">
    <span class="search__eyebrow">§ Search the corpus</span>
    <h1 class="search__title">
      {#if ql}
        Results for <em class="search__title-q">"{q}"</em>
      {:else}
        <em>Search</em> the corpus
      {/if}
    </h1>
    <div class="search__field">
      <Input
        size="lg"
        placeholder="Search title, author, narrator…"
        bind:value={q}
        onkeydown={onKey}
      />
    </div>
    {#if ql}
      <div class="search__counts">
        <span class="search__count">{matches.length} books</span>
        <span class="search__count">{passageHits.length} passages</span>
        <span class="search__count">{narratorHits.length} narrators</span>
      </div>
    {/if}
  </header>

  <div class="search__layout">
    <div class="search__results">
      {#if narratorHits.length}
        <section class="search__section">
          <h2 class="search__section-head">
            <span class="search__section-icon">◉</span>
            Narrators
            <span class="search__section-count">{narratorHits.length}</span>
          </h2>
          <ul class="search__nlist">
            {#each narratorHits as n (n.name)}
              <li class="narr">
                <div class="narr__top">
                  <span class="narr__ar" dir="rtl">{n.nameAr}</span>
                  <span class="narr__en">{n.name}</span>
                  <span class="narr__grade">trustworthy</span>
                </div>
                <div class="narr__meta">
                  {n.role} · d. {n.d} AH · {n.count.toLocaleString()} reports in graph
                </div>
              </li>
            {/each}
          </ul>
        </section>
      {/if}

      {#if passageHits.length}
        <section class="search__section">
          <h2 class="search__section-head">
            <span class="search__section-icon">⟫</span>
            Passages
            <span class="search__section-count">{passageHits.length}</span>
          </h2>
          <ul class="search__plist">
            {#each passageHits as p (p.urn + p.page)}
              <li class="pass">
                <Pressable class="pass__btn" onclick={() => goto(`/reader/${p.urn}/${p.page}`)}>
                  <div class="pass__head">
                    <span class="pass__book-ar" dir="rtl">{p.bookAr}</span>
                    <span class="pass__book-en">{p.bookEn}</span>
                    <span class="pass__page">page {p.page}</span>
                  </div>
                  <div class="pass__snippet-ar" dir="rtl">{p.snippetAr}</div>
                  <div class="pass__snippet-en">{p.snippetEn}</div>
                </Pressable>
              </li>
            {/each}
          </ul>
        </section>
      {/if}

      <section class="search__section">
        <h2 class="search__section-head">
          <span class="search__section-icon">≡</span>
          Books
          <span class="search__section-count">{matches.length}</span>
        </h2>

        {#if matches.length === 0}
          <div class="search__empty">No books match this query.</div>
        {:else}
          <div class="search__groups">
            {#each grouped as [slug, bs] (slug)}
              {@const cat = findCat(slug)}
              <div class="search__group">
                <div class="search__group-head">
                  <span class="search__group-label">{cat?.label ?? slug}</span>
                  <span class="search__group-n">{bs.length}</span>
                </div>
                <div class="search__group-grid">
                  {#each bs as b (b.urn)}
                    <BookCard
                      book={{
                        urn: b.urn,
                        titleArabic: b.titleAr,
                        titleLatin: b.titleEn,
                        author: b.author,
                        authorAh: b.deathYearAh,
                        pages: b.pageCount,
                        sect: b.sect,
                        canonical: b.canonical,
                      }}
                      layout="card"
                      onSelect={(urn) => goto(`/reader/${urn}/109`)}
                    />
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </section>
    </div>

    <SearchScope counts={{ total: matches.length, primary, sunni: sectSunni, imami: sectImami }} />
  </div>
</div>

<style>
  .search {
    max-width: 1280px;
    margin: 0 auto;
    padding: 48px 32px 96px;
    position: relative;
    z-index: 1;
  }
  .search__head {
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding: 28px 0 24px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .search__eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent);
    letter-spacing: 0.22em;
    text-transform: uppercase;
  }
  .search__title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 500;
    color: var(--color-fg-1);
    letter-spacing: var(--tracking-tight);
  }
  .search__title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }
  .search__title-q {
    font-style: italic;
    color: var(--color-accent);
  }
  .search__field {
    max-width: 640px;
  }
  .search__counts {
    display: flex;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }
  .search__count {
    border: 1px solid var(--color-border-1);
    padding: 4px 10px;
    border-radius: var(--radius-full);
  }

  .search__layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 280px;
    gap: 32px;
  }
  @media (max-width: 980px) {
    .search__layout {
      grid-template-columns: 1fr;
    }
  }

  .search__results {
    display: flex;
    flex-direction: column;
    gap: 48px;
    min-width: 0;
  }
  .search__section {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .search__section-head {
    margin: 0;
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--color-border-1);
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-xl);
    color: var(--color-fg-1);
    font-weight: 500;
  }
  .search__section-icon {
    color: var(--color-accent);
    font-style: normal;
  }
  .search__section-count {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-style: normal;
  }

  .search__nlist,
  .search__plist {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .narr {
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-md);
    background: var(--color-bg-1);
    padding: 14px 18px;
    transition: border-color var(--duration-fast) var(--ease-standard);
  }
  .narr:hover {
    border-color: var(--color-border-strong);
  }
  .narr__top {
    display: flex;
    align-items: baseline;
    gap: 12px;
    flex-wrap: wrap;
  }
  .narr__ar {
    font-family: var(--font-arabic);
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--color-fg-1);
  }
  .narr__en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-fg-2);
  }
  .narr__grade {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-success);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }
  .narr__meta {
    margin-top: 4px;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-fg-3);
  }

  :global(.pass__btn) {
    display: block;
    width: 100%;
    text-align: left;
    padding: 14px 18px;
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-md);
    background: var(--color-bg-1);
    color: inherit;
    cursor: pointer;
    transition: border-color var(--duration-fast) var(--ease-standard);
  }
  :global(.pass__btn:hover) {
    border-color: var(--color-accent);
  }
  .pass__head {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 8px;
  }
  .pass__book-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--color-fg-1);
  }
  .pass__book-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-fg-2);
  }
  .pass__page {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.14em;
  }
  .pass__snippet-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-base);
    line-height: 1.85;
    color: var(--color-fg-1);
    margin-bottom: 6px;
  }
  .pass__snippet-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-fg-2);
    line-height: 1.5;
  }

  .search__groups {
    display: flex;
    flex-direction: column;
    gap: 28px;
  }
  .search__group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .search__group-head {
    display: flex;
    align-items: baseline;
    gap: 12px;
  }
  .search__group-label {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-2);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }
  .search__group-n {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
  }
  .search__group-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 18px;
  }
  .search__empty {
    padding: 48px;
    border: 1px dashed var(--color-border-1);
    border-radius: var(--radius-lg);
    text-align: center;
    font-family: var(--font-display);
    font-style: italic;
    color: var(--color-fg-3);
  }
</style>
