<!--
  Library category page — header (breadcrumb + Arabic+Latin titles +
  stats), filter rail, BookCard grid. Uses the SSOT BookCard so any
  visual tweak in lib/design-system/composed/BookCard.svelte propagates
  here without a forked render path.
-->
<script lang="ts">
  import { page } from '$app/state';
  import { Breadcrumb, BookCard, FilterPill, Input, Text } from '$lib/design-system';
  import { DOMAINS, BOOKS } from '$lib/fixtures';
  import type { Sect } from '$lib/design-system';

  const slug = $derived(page.params.category ?? '');

  const catMeta = $derived.by(() => {
    for (const d of DOMAINS) {
      for (const c of d.categories) {
        if (c.slug === slug) return { ...c, domain: d };
      }
    }
    return null;
  });

  // For prototype: combine real books in the category with synthesized
  // fillers from BOOKS so the grid is populated. Real backend will replace.
  const books = $derived.by(() => {
    const real = BOOKS.filter((b) => b.category === slug);
    const need = Math.max(0, Math.min(8, (catMeta?.count ?? 8) - real.length));
    const filler = Array.from({ length: need }, (_, i) => {
      const base = BOOKS[i % BOOKS.length];
      if (!base) return null;
      return { ...base, urn: `${base.urn}-${i}`, category: slug };
    }).filter((b): b is (typeof BOOKS)[number] => b !== null);
    return [...real, ...filler];
  });

  let filter = $state('');
  let sort = $state<'canonical' | 'death' | 'pages' | 'author'>('canonical');
  let sect = $state<'all' | Sect>('all');

  const filtered = $derived.by(() => {
    const q = filter.toLowerCase();
    const list = books.filter((b) => {
      if (q) {
        const hay = (b.titleAr + ' ' + b.titleEn + ' ' + b.author).toLowerCase();
        if (!hay.includes(q)) return false;
      }
      if (sect !== 'all' && b.sect !== sect) return false;
      return true;
    });
    const score = (s: string) => (s === 'primary' ? -1 : s === 'secondary' ? 0 : 1);
    return [...list].sort((a, b) => {
      if (sort === 'canonical') return score(a.canonical) - score(b.canonical);
      if (sort === 'death') return (a.deathYearAh ?? 9999) - (b.deathYearAh ?? 9999);
      if (sort === 'pages') return b.pageCount - a.pageCount;
      if (sort === 'author') return a.author.localeCompare(b.author);
      return 0;
    });
  });

  const sortOptions: { v: typeof sort; l: string }[] = [
    { v: 'canonical', l: 'Canonical' },
    { v: 'death', l: 'Death year' },
    { v: 'pages', l: 'Pages' },
    { v: 'author', l: 'Author A–Z' },
  ];
  const sects: { v: 'all' | Sect; l: string }[] = [
    { v: 'all', l: 'All' },
    { v: 'imami', l: 'Imami' },
    { v: 'sunni', l: 'Sunni' },
    { v: 'zaidi', l: 'Zaidi' },
    { v: 'ismaili', l: 'Ismaili' },
  ];

  const indexedPages = $derived(Math.round((catMeta?.count ?? 0) * 184).toLocaleString());
</script>

<svelte:head>
  <title>{catMeta?.label ?? 'Category'} · Library · Shia Online Library</title>
</svelte:head>

<div class="cat">
  {#if !catMeta}
    <div class="cat__empty">
      <Text tone="secondary">Category not found.</Text>
    </div>
  {:else}
    <Breadcrumb
      items={[
        { label: 'Browse', href: '/' },
        { label: 'Library', href: '/library' },
        { label: catMeta.domain.label, href: '/library' },
        { label: catMeta.label },
      ]}
    />

    <header class="cat__head">
      <span class="cat__section">§ {catMeta.domain.label}</span>
      <span class="cat__title-ar" dir="rtl">{catMeta.labelAr}</span>
      <h1 class="cat__title-en">{catMeta.label}</h1>
      <span class="cat__stats">
        {catMeta.count} works · indexed across {indexedPages} pages
      </span>
    </header>

    <div class="cat__filters">
      <div class="cat__filter-search">
        <Input bind:value={filter} placeholder="Search in this category…" />
      </div>

      <div class="cat__filter-group">
        <span class="cat__filter-label">Sort</span>
        {#each sortOptions as o (o.v)}
          <FilterPill active={sort === o.v} onclick={() => (sort = o.v)}>{o.l}</FilterPill>
        {/each}
      </div>

      <div class="cat__filter-group">
        <span class="cat__filter-label">Affiliation</span>
        {#each sects as s (s.v)}
          <FilterPill active={sect === s.v} onclick={() => (sect = s.v)}>{s.l}</FilterPill>
        {/each}
      </div>

      <span class="cat__count">{filtered.length} of {books.length}</span>
    </div>

    {#if filtered.length === 0}
      <div class="cat__empty">
        <Text tone="secondary">No books match this filter.</Text>
      </div>
    {:else}
      <div class="cat__grid">
        {#each filtered as b (b.urn)}
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
            onSelect={(urn) => window.location.assign(`/book/${urn}`)}
          />
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .cat {
    max-width: 1280px;
    margin: 0 auto;
    padding: 48px 32px 96px;
    position: relative;
    z-index: 1;
  }

  .cat__head {
    display: grid;
    grid-template-columns: auto;
    gap: 12px;
    padding: 32px 0 28px;
    margin-bottom: 28px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .cat__section {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent);
    letter-spacing: 0.22em;
    text-transform: uppercase;
  }
  .cat__title-ar {
    font-family: var(--font-arabic);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    color: var(--color-fg-1);
    line-height: 1.1;
    text-align: right;
  }
  .cat__title-en {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: clamp(1.5rem, 2.5vw, 2rem);
    font-weight: 500;
    color: var(--color-fg-2);
    letter-spacing: var(--tracking-tight);
  }
  .cat__stats {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }

  .cat__filters {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 14px;
    padding-bottom: 24px;
    margin-bottom: 28px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .cat__filter-search {
    flex: 1;
    min-width: 240px;
  }
  .cat__filter-group {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }
  .cat__filter-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-right: 4px;
  }
  .cat__count {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-left: auto;
  }

  .cat__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 22px;
  }

  .cat__empty {
    padding: 64px;
    text-align: center;
    border: 1px dashed var(--color-border-1);
    border-radius: var(--radius-lg);
  }
</style>
