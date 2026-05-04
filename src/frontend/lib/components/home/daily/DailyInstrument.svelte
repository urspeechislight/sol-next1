<!--
  The Daily Instrument — three coordinated live visualizations sharing
  one rhythmic heartbeat. Replaces the static "verse / hadith / book of
  the day" cards with a single working instrument.
-->
<script lang="ts">
  import { DAILY, BOOKS, findBook } from '$lib/fixtures';
  import RecitationPanel from './RecitationPanel.svelte';
  import IsnadPanel from './IsnadPanel.svelte';
  import FolioPanel from './FolioPanel.svelte';
  import HeartbeatStrip from './HeartbeatStrip.svelte';

  // Shared 1Hz heartbeat — drives the tick strip below.
  let tick = $state(0);
  $effect(() => {
    const id = setInterval(() => {
      tick += 1;
    }, 1000);
    return () => clearInterval(id);
  });

  const dailyBook = $derived(findBook(DAILY.book.urn) ?? BOOKS[0]);
</script>

<section class="instrument" aria-labelledby="instrument-head">
  <header class="instrument__head">
    <div class="instrument__head-left">
      <span class="instrument__head-section">§ II</span>
      <h2 id="instrument-head" class="instrument__head-title">
        <em>The</em> Daily Instrument
      </h2>
    </div>
    <div class="instrument__head-right">
      <span class="instrument__head-date" dir="rtl">{DAILY.date.hijri}</span>
      <span class="instrument__head-sep">·</span>
      <span class="instrument__head-date">{DAILY.date.gregorian}</span>
      <span class="instrument__head-sep">·</span>
      <span class="instrument__head-issue">№ 0421</span>
    </div>
  </header>

  <div class="instrument__deck">
    <RecitationPanel verse={DAILY.verse} />
    <div class="instrument__divider" aria-hidden="true"></div>
    <IsnadPanel hadith={DAILY.hadith} />
    <div class="instrument__divider" aria-hidden="true"></div>
    {#if dailyBook}
      <FolioPanel book={dailyBook} daily={DAILY.book} />
    {/if}
  </div>

  <HeartbeatStrip {tick} />
</section>

<style>
  .instrument {
    position: relative;
    z-index: 1;
    max-width: 1280px;
    margin: 64px auto 0;
    padding: 0 32px;
    color: var(--color-fg-1);
  }

  .instrument__head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 24px;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--color-border-1);
    flex-wrap: wrap;
  }
  .instrument__head-left {
    display: flex;
    align-items: baseline;
    gap: 18px;
  }
  .instrument__head-section {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    color: var(--color-accent);
    text-transform: uppercase;
  }
  .instrument__head-title {
    margin: 0;
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 2vw, 1.875rem);
    font-weight: 500;
    letter-spacing: var(--tracking-tight);
    color: var(--color-fg-1);
  }
  .instrument__head-title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }
  .instrument__head-right {
    display: flex;
    align-items: baseline;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-fg-3);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    flex-wrap: wrap;
  }
  .instrument__head-date {
    color: var(--color-fg-2);
  }
  .instrument__head-date[dir='rtl'] {
    font-family: var(--font-arabic);
    font-size: 13px;
    text-transform: none;
    color: var(--color-accent);
  }
  .instrument__head-sep {
    color: var(--color-accent);
    opacity: 0.45;
  }
  .instrument__head-issue {
    color: var(--color-accent);
    letter-spacing: 0.18em;
  }

  .instrument__deck {
    display: grid;
    grid-template-columns: 1fr 1px 1fr 1px 0.85fr;
    gap: 28px;
    padding: 28px 0;
  }
  .instrument__divider {
    background: linear-gradient(to bottom, transparent, var(--color-border-2), transparent);
    width: 1px;
  }

  @media (max-width: 1024px) {
    .instrument__deck {
      grid-template-columns: 1fr;
      gap: 36px;
    }
    .instrument__divider {
      width: 100%;
      height: 1px;
      background: linear-gradient(to right, transparent, var(--color-border-2), transparent);
    }
  }
  @media (max-width: 640px) {
    .instrument {
      padding: 0 20px;
      margin-top: 48px;
    }
  }
</style>
