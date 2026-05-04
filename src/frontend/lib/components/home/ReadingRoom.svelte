<!--
  Reading Room — featured books as horizontally-scrollable manuscript
  vitrines. Each card has an illuminated codex face (gold corner
  ornaments + Arabic title + Latin italic + author) over a colored
  spine accent. Click to open the book.
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { Pressable, SectBadge, CanonicalBadge } from '$lib/design-system';
  import { BOOKS, DAILY } from '$lib/fixtures';

  // Show the rotation list (curated for today) first, fall back to BOOKS order.
  const ordered = $derived.by(() => {
    const byUrn = new Map(BOOKS.map((b) => [b.urn, b]));
    const out = [];
    for (const urn of DAILY.rotation) {
      const b = byUrn.get(urn);
      if (b) out.push(b);
    }
    for (const b of BOOKS) if (!DAILY.rotation.includes(b.urn)) out.push(b);
    return out;
  });

  let trackEl: HTMLElement | undefined = $state();

  function scroll(direction: -1 | 1) {
    if (!trackEl) return;
    const w = trackEl.clientWidth;
    trackEl.scrollBy({ left: direction * w * 0.85, behavior: 'smooth' });
  }
</script>

<section class="rr" aria-labelledby="rr-head">
  <header class="rr__head">
    <div class="rr__head-left">
      <span class="rr__head-section">§ III</span>
      <h2 id="rr-head" class="rr__head-title">
        <em>The</em> Reading Room
      </h2>
    </div>
    <div class="rr__head-right">
      <span class="rr__head-meta">In rotation today</span>
      <Pressable class="rr__nav" aria-label="Previous" onclick={() => scroll(-1)}>‹</Pressable>
      <Pressable class="rr__nav" aria-label="Next" onclick={() => scroll(1)}>›</Pressable>
    </div>
  </header>

  <div bind:this={trackEl} class="rr__track">
    {#each ordered as b (b.urn)}
      <Pressable class="vitrine" aria-label={b.titleEn} onclick={() => goto(`/book/${b.urn}`)}>
        <div class="vitrine__cover">
          <span class="vitrine__corner vitrine__corner--tl"></span>
          <span class="vitrine__corner vitrine__corner--tr"></span>
          <span class="vitrine__corner vitrine__corner--bl"></span>
          <span class="vitrine__corner vitrine__corner--br"></span>
          <span class="vitrine__spine"></span>
          <div class="vitrine__cover-content">
            <span class="vitrine__cover-ar" dir="rtl">{b.titleAr}</span>
            <span class="vitrine__cover-divider"></span>
            <span class="vitrine__cover-en">{b.titleEn}</span>
            <span class="vitrine__cover-author">{b.author}</span>
          </div>
        </div>

        <div class="vitrine__meta">
          <div class="vitrine__meta-row">
            <span class="vitrine__urn">{b.urn}</span>
            <span class="vitrine__pages">{b.pageCount} pp</span>
          </div>
          <div class="vitrine__badges">
            <SectBadge sect={b.sect} />
            <CanonicalBadge tier={b.canonical} />
          </div>
        </div>
      </Pressable>
    {/each}
  </div>
</section>

<style>
  .rr {
    position: relative;
    z-index: 1;
    max-width: 1280px;
    margin: 64px auto 0;
    padding: 0 32px;
    color: var(--color-fg-1);
  }

  .rr__head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 24px;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--color-border-1);
    flex-wrap: wrap;
  }
  .rr__head-left {
    display: flex;
    align-items: baseline;
    gap: 18px;
  }
  .rr__head-section {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    color: var(--color-accent);
    text-transform: uppercase;
  }
  .rr__head-title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 2vw, 1.875rem);
    font-weight: 500;
    color: var(--color-fg-1);
  }
  .rr__head-title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }
  .rr__head-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .rr__head-meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    letter-spacing: 0.16em;
    text-transform: uppercase;
  }
  :global(.rr__nav) {
    width: 32px;
    height: 32px;
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-full);
    background: var(--color-bg-1);
    color: var(--color-accent);
    cursor: pointer;
    font-size: var(--text-xl);
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition:
      border-color var(--duration-fast) var(--ease-standard),
      background var(--duration-fast) var(--ease-standard);
  }
  :global(.rr__nav:hover) {
    border-color: var(--color-accent);
    background: var(--color-accent-soft);
  }

  .rr__track {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: minmax(180px, 220px);
    gap: 22px;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 8px 4px 24px;
    scroll-snap-type: x mandatory;
    scrollbar-width: thin;
  }
  .rr__track::-webkit-scrollbar {
    height: 6px;
  }
  .rr__track::-webkit-scrollbar-thumb {
    background: var(--color-border-2);
    border-radius: 3px;
  }

  :global(.vitrine) {
    display: flex;
    flex-direction: column;
    gap: 12px;
    text-align: left;
    cursor: pointer;
    background: transparent;
    border: none;
    padding: 0;
    scroll-snap-align: start;
  }

  .vitrine__cover {
    position: relative;
    aspect-ratio: 3 / 4;
    border: 1px solid var(--color-border-strong);
    border-radius: var(--radius-sm);
    background:
      radial-gradient(ellipse at 50% 0%, var(--color-accent-soft) 0%, transparent 70%),
      linear-gradient(180deg, var(--color-bg-night-1) 0%, var(--color-bg-night-2) 100%);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition:
      transform var(--duration-normal) var(--ease-standard),
      box-shadow var(--duration-normal) var(--ease-standard);
  }
  :global(.vitrine:hover) .vitrine__cover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
  }
  .vitrine__spine {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 6px;
    background: linear-gradient(to right, var(--color-crimson) 0%, transparent 100%);
    opacity: 0.55;
  }
  .vitrine__corner {
    position: absolute;
    width: 10px;
    height: 10px;
    border: 1px solid var(--color-accent);
    opacity: 0.7;
  }
  .vitrine__corner--tl {
    top: 8px;
    left: 12px;
    border-right: none;
    border-bottom: none;
  }
  .vitrine__corner--tr {
    top: 8px;
    right: 8px;
    border-left: none;
    border-bottom: none;
  }
  .vitrine__corner--bl {
    bottom: 8px;
    left: 12px;
    border-right: none;
    border-top: none;
  }
  .vitrine__corner--br {
    bottom: 8px;
    right: 8px;
    border-left: none;
    border-top: none;
  }

  .vitrine__cover-content {
    position: absolute;
    inset: 22px 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    text-align: center;
  }
  .vitrine__cover-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--color-fg-1);
    line-height: 1.2;
    text-wrap: balance;
  }
  .vitrine__cover-divider {
    width: 24px;
    height: 1px;
    background: var(--color-accent);
  }
  .vitrine__cover-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-accent);
    line-height: 1.2;
  }
  .vitrine__cover-author {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--color-fg-3);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .vitrine__meta {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .vitrine__meta-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .vitrine__urn {
    color: var(--color-accent);
  }
  .vitrine__badges {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
  }
</style>
