<!--
  Library index — full corpus broken down by the 7 knowledge domains
  and their 39 categories. Click into any category to see the book grid.
-->
<script lang="ts">
  import { Breadcrumb, Text } from '$lib/design-system';
  import { DOMAINS } from '$lib/fixtures';

  const totalWorks = $derived(
    DOMAINS.reduce((a, d) => a + d.categories.reduce((aa, c) => aa + c.count, 0), 0),
  );
</script>

<svelte:head>
  <title>Library · Shia Online Library</title>
</svelte:head>

<div class="lib-index">
  <Breadcrumb items={[{ label: 'Browse', href: '/' }, { label: 'Library' }]} />

  <header class="lib-index__head">
    <span class="lib-index__eyebrow">§ The Library</span>
    <h1 class="lib-index__title">
      <em>The</em> Corpus
    </h1>
    <p class="lib-index__sub">
      <span dir="rtl" class="lib-index__sub-ar">المكتبة</span>
      <span class="lib-index__sub-meta">
        {DOMAINS.length} domains · {DOMAINS.reduce((a, d) => a + d.categories.length, 0)} categories
        · {totalWorks} works
      </span>
    </p>
  </header>

  <div class="lib-index__domains">
    {#each DOMAINS as d, i (d.id)}
      {@const works = d.categories.reduce((a, c) => a + c.count, 0)}
      <section class="lib-index__domain">
        <header class="lib-index__domain-head">
          <span class="lib-index__domain-num">{String(i + 1).padStart(2, '0')}</span>
          <div class="lib-index__domain-titles">
            <span dir="rtl" class="lib-index__domain-ar">{d.labelAr}</span>
            <h2 class="lib-index__domain-en">{d.label}</h2>
          </div>
          <span class="lib-index__domain-count">{works} works</span>
        </header>
        <p class="lib-index__domain-blurb">{d.blurb}</p>

        <ul class="lib-index__cats">
          {#each d.categories as c (c.slug)}
            <li class="lib-index__cat">
              <a class="lib-index__cat-link" href={`/library/${c.slug}`}>
                <span class="lib-index__cat-en">{c.label}</span>
                <span class="lib-index__cat-ar" dir="rtl">{c.labelAr}</span>
                <span class="lib-index__cat-n">{c.count}</span>
                <span class="lib-index__cat-arrow" aria-hidden="true">→</span>
              </a>
            </li>
          {/each}
        </ul>
      </section>
    {/each}
  </div>

  {#if false}
    <Text size="sm">unused</Text>
  {/if}
</div>

<style>
  .lib-index {
    max-width: 1280px;
    margin: 0 auto;
    padding: 48px 32px 96px;
    position: relative;
    z-index: 1;
  }
  .lib-index__head {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 32px 0 28px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .lib-index__eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent);
    letter-spacing: 0.22em;
    text-transform: uppercase;
  }
  .lib-index__title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 5vw, 3.75rem);
    font-weight: 500;
    color: var(--color-fg-1);
    letter-spacing: var(--tracking-tight);
  }
  .lib-index__title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }
  .lib-index__sub {
    margin: 0;
    display: flex;
    align-items: baseline;
    gap: 16px;
    flex-wrap: wrap;
  }
  .lib-index__sub-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-2xl);
    color: var(--color-accent);
    font-weight: 700;
  }
  .lib-index__sub-meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }

  .lib-index__domains {
    display: flex;
    flex-direction: column;
    gap: 56px;
  }
  .lib-index__domain {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .lib-index__domain-head {
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 18px;
    align-items: baseline;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .lib-index__domain-num {
    font-family: var(--font-display);
    font-style: italic;
    font-size: clamp(2rem, 3vw, 2.5rem);
    color: var(--color-accent);
    line-height: 1;
  }
  .lib-index__domain-titles {
    display: flex;
    align-items: baseline;
    gap: 14px;
    flex-wrap: wrap;
  }
  .lib-index__domain-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-fg-1);
  }
  .lib-index__domain-en {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-xl);
    font-weight: 500;
    color: var(--color-fg-2);
  }
  .lib-index__domain-count {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .lib-index__domain-blurb {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-fg-2);
    max-width: 720px;
  }

  .lib-index__cats {
    list-style: none;
    margin: 6px 0 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1px;
    background: var(--color-border-1);
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-sm);
    overflow: hidden;
  }
  .lib-index__cat {
    background: var(--color-bg-1);
  }
  .lib-index__cat-link {
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    gap: 12px;
    align-items: baseline;
    padding: 14px 16px;
    text-decoration: none;
    color: inherit;
    transition: background var(--duration-fast) var(--ease-standard);
  }
  .lib-index__cat-link:hover {
    background: var(--color-bg-2);
  }
  .lib-index__cat-en {
    font-family: var(--font-display);
    font-size: var(--text-sm);
    color: var(--color-fg-1);
  }
  .lib-index__cat-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    color: var(--color-accent);
  }
  .lib-index__cat-n {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.14em;
  }
  .lib-index__cat-arrow {
    color: var(--color-fg-3);
    transition:
      color var(--duration-fast) var(--ease-standard),
      transform var(--duration-fast) var(--ease-standard);
  }
  .lib-index__cat-link:hover .lib-index__cat-arrow {
    color: var(--color-accent);
    transform: translateX(2px);
  }
</style>
