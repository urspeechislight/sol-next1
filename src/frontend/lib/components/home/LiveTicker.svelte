<!--
  Live "now indexing" ticker — pulsing dot + cycling work title every
  3.2s, suggesting a live pipeline behind the page. Reads from BOOKS
  fixture as the rotation source.
-->
<script lang="ts">
  import type { Book } from '$lib/fixtures';

  interface Props {
    books: Book[];
    interval?: number | undefined;
  }
  let { books, interval = 3200 }: Props = $props();

  let idx = $state(0);
  const current = $derived(books[idx % books.length]);

  $effect(() => {
    const t = setInterval(() => {
      idx = (idx + 1) % books.length;
    }, interval);
    return () => clearInterval(t);
  });
</script>

<div class="ticker" aria-live="polite">
  <span class="ticker__dot" aria-hidden="true"></span>
  <span class="ticker__label">Now indexing</span>
  {#if current}
    {#key current.urn}
      <span class="ticker__title">
        <span class="ticker__title-en">{current.titleEn}</span>
        <span class="ticker__title-ar" dir="rtl">{current.titleAr}</span>
      </span>
    {/key}
  {/if}
</div>

<style>
  .ticker {
    display: inline-flex;
    align-items: baseline;
    gap: 10px;
    padding: 8px 14px;
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-full);
    background: var(--color-bg-1);
    backdrop-filter: blur(6px);
    align-self: flex-start;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
  }
  .ticker__dot {
    width: 8px;
    height: 8px;
    border-radius: var(--radius-full);
    background: var(--color-success);
    box-shadow: 0 0 12px var(--color-success);
    align-self: center;
    animation: ticker-pulse 1.6s ease-in-out infinite;
  }
  @keyframes ticker-pulse {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.55;
      transform: scale(0.85);
    }
  }
  .ticker__label {
    color: var(--color-fg-3);
    letter-spacing: var(--tracking-wide);
    text-transform: uppercase;
  }
  .ticker__title {
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
    animation: ticker-fade 0.5s ease-out;
  }
  @keyframes ticker-fade {
    from {
      opacity: 0;
      transform: translateY(2px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .ticker__title-en {
    color: var(--color-fg-1);
    font-style: italic;
    font-family: var(--font-display);
    font-size: var(--text-sm);
  }
  .ticker__title-ar {
    color: var(--color-accent);
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
  }
</style>
