<!--
  Stats marquee — corpus measured in italic Cormorant numerals,
  drifting horizontally on a slow loop. Decorative section that gives
  the page a sense of scale without bombarding with metrics.
-->
<script lang="ts">
  import { DOMAINS, BOOKS } from '$lib/fixtures';

  const totalCategories = $derived(DOMAINS.reduce((a, d) => a + d.categories.length, 0));
  const totalWorks = $derived(
    DOMAINS.reduce((a, d) => a + d.categories.reduce((aa, c) => aa + c.count, 0), 0),
  );
  const totalPages = $derived(BOOKS.reduce((a, b) => a + b.pageCount, 0));
  const totalAuthors = $derived(new Set(BOOKS.map((b) => b.author)).size);

  const items = $derived([
    { n: totalWorks.toLocaleString(), l: 'works indexed' },
    { n: DOMAINS.length, l: 'knowledge domains' },
    { n: totalCategories, l: 'categories' },
    { n: totalPages.toLocaleString(), l: 'pages parsed' },
    { n: totalAuthors, l: 'authors' },
    { n: '12c', l: 'centuries traversed' },
    { n: '4', l: 'sects represented' },
    { n: '∞', l: 'paths of transmission' },
  ]);

  // Duplicate so the marquee loop is seamless.
  const loop = $derived([...items, ...items]);
</script>

<section class="stats" aria-labelledby="stats-head">
  <header class="stats__head">
    <span class="stats__section">§ IV</span>
    <h2 id="stats-head" class="stats__title"><em>The</em> Corpus, in Numbers</h2>
  </header>

  <div class="stats__rail" aria-hidden="true">
    <div class="stats__strip">
      {#each loop as item, i (i)}
        <span class="stats__item">
          <span class="stats__num">{item.n}</span>
          <span class="stats__label">{item.l}</span>
          <span class="stats__sep">✦</span>
        </span>
      {/each}
    </div>
  </div>
</section>

<style>
  .stats {
    position: relative;
    z-index: 1;
    max-width: 1280px;
    margin: 64px auto 0;
    padding: 0 32px;
  }
  .stats__head {
    display: flex;
    align-items: baseline;
    gap: 18px;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--color-border-1);
  }
  .stats__section {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    color: var(--color-accent);
    text-transform: uppercase;
  }
  .stats__title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 2vw, 1.875rem);
    font-weight: 500;
    color: var(--color-fg-1);
  }
  .stats__title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }

  .stats__rail {
    overflow: hidden;
    mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
    padding: 12px 0 22px;
  }
  .stats__strip {
    display: inline-flex;
    align-items: baseline;
    gap: 36px;
    white-space: nowrap;
    animation: stats-drift 60s linear infinite;
  }
  @keyframes stats-drift {
    from {
      transform: translateX(0);
    }
    to {
      transform: translateX(-50%);
    }
  }

  .stats__item {
    display: inline-flex;
    align-items: baseline;
    gap: 10px;
  }
  .stats__num {
    font-family: var(--font-display);
    font-style: italic;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 500;
    color: var(--color-accent);
    letter-spacing: var(--tracking-tight);
  }
  .stats__label {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-fg-2);
  }
  .stats__sep {
    color: var(--color-accent);
    opacity: 0.4;
    font-size: var(--text-sm);
  }
</style>
