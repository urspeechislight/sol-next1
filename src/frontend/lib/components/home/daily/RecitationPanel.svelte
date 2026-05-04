<!--
  Recitation panel — verse of the day with word-by-word reveal animation
  and a tafsir crossfader beneath. Click the verse to replay.
-->
<script lang="ts">
  import { Pressable } from '$lib/design-system';
  import type { VerseOfDay } from '$lib/fixtures';

  interface Props {
    verse: VerseOfDay;
  }
  let { verse }: Props = $props();

  const words = $derived(verse.ayahAr.split(/\s+/).filter(Boolean));
  const TOTAL_MS = 12000;
  const HOLD_MS = 3000;
  const CYCLE = TOTAL_MS + HOLD_MS;

  let t0 = $state(0);
  let now = $state(0);

  $effect(() => {
    t0 = performance.now();
    let raf = 0;
    const frame = () => {
      now = performance.now();
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  });

  const elapsed = $derived((now - t0) % CYCLE || 0);
  const reveal = $derived(Math.min(1, elapsed / TOTAL_MS));
  const wordsRevealed = $derived(Math.floor(reveal * words.length));

  let tafsirIdx = $state(0);
  $effect(() => {
    const id = setInterval(() => {
      tafsirIdx = (tafsirIdx + 1) % verse.tafsirs.length;
    }, 6000);
    return () => clearInterval(id);
  });

  function replay() {
    t0 = performance.now();
  }
</script>

<article class="panel">
  <div class="panel__eyebrow">
    <span class="panel__eyebrow-num">I</span>
    <span class="panel__eyebrow-label">Recitation</span>
    <span class="panel__eyebrow-live" aria-hidden="true"></span>
    <span class="panel__eyebrow-sub">Sūra {verse.surahN} · Āya {verse.ayahN}</span>
  </div>

  <h3 class="panel__title" dir="rtl">
    <span class="panel__title-ar">{verse.surahAr}</span>
    <span class="panel__title-en">{verse.surah}</span>
  </h3>

  <Pressable class="cartouche" onclick={replay} title="Replay the recitation">
    <span class="cartouche__words" dir="rtl">
      {#each words as w, i (i)}
        <span
          class="cartouche__word"
          class:reveal={i < wordsRevealed}
          class:cursor={i === wordsRevealed - 1}
        >
          {w}{i < words.length - 1 ? ' ' : ''}
        </span>
      {/each}
    </span>
    <span class="cartouche__progress" style:width="{(reveal * 100).toFixed(2)}%"></span>
  </Pressable>

  <p class="recitation__en">{verse.ayahEn}</p>

  <div class="tafsir">
    <div class="tafsir__head">
      <span class="tafsir__label">Tafsīr</span>
      <div class="tafsir__dots" role="tablist">
        {#each verse.tafsirs as _t, i (i)}
          <Pressable
            class="tafsir__dot {i === tafsirIdx ? 'is-active' : ''}"
            aria-label={`Show tafsir ${i + 1}`}
            onclick={() => (tafsirIdx = i)}
          />
        {/each}
      </div>
    </div>
    <div class="tafsir__stage">
      {#each verse.tafsirs as t, i (t.urn)}
        <div class="tafsir__card" class:active={i === tafsirIdx}>
          <div class="tafsir__meta">
            <span class="tafsir__book">{t.book}</span>
            <span class="tafsir__author"> · {t.author}</span>
          </div>
          <p class="tafsir__text">{t.excerptEn}</p>
        </div>
      {/each}
    </div>
  </div>
</article>

<style>
  .panel {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-width: 0;
  }
  .panel__eyebrow {
    display: flex;
    align-items: baseline;
    gap: 10px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .panel__eyebrow-num {
    color: var(--color-accent);
    font-weight: 600;
  }
  .panel__eyebrow-label {
    color: var(--color-fg-2);
  }
  .panel__eyebrow-live {
    width: 6px;
    height: 6px;
    border-radius: var(--radius-full);
    background: var(--color-success);
    box-shadow: 0 0 8px var(--color-success);
    animation: panel-pulse 1.6s ease-in-out infinite;
    align-self: center;
  }
  .panel__eyebrow-sub {
    color: var(--color-fg-3);
    margin-left: auto;
  }
  @keyframes panel-pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.4;
    }
  }

  .panel__title {
    margin: 0;
    display: flex;
    align-items: baseline;
    justify-content: flex-end;
    gap: 12px;
    font-family: var(--font-arabic);
    font-size: var(--text-2xl);
    color: var(--color-fg-1);
  }
  .panel__title-ar {
    font-weight: 700;
  }
  .panel__title-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-accent);
  }

  :global(.cartouche) {
    position: relative;
    display: block;
    text-align: right;
    padding: 22px 18px 26px;
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-md);
    background:
      radial-gradient(ellipse at 50% 0%, var(--color-accent-soft), transparent 70%),
      var(--color-bg-1);
    cursor: pointer;
    transition: border-color var(--duration-normal) var(--ease-standard);
    width: 100%;
  }
  :global(.cartouche:hover) {
    border-color: var(--color-border-strong);
  }
  .cartouche__words {
    display: block;
    font-family: var(--font-arabic);
    font-size: var(--text-xl);
    line-height: 2.2;
    color: var(--color-fg-1);
    direction: rtl;
  }
  .cartouche__word {
    opacity: 0.18;
    transition:
      opacity 380ms ease,
      color 380ms ease;
  }
  .cartouche__word.reveal {
    opacity: 1;
    color: var(--color-fg-1);
  }
  .cartouche__word.cursor {
    color: var(--color-accent);
    text-shadow: 0 0 14px var(--color-accent-soft);
  }
  .cartouche__progress {
    position: absolute;
    left: 0;
    bottom: 0;
    height: 1px;
    background: var(--color-accent);
    transition: width 100ms linear;
  }

  .recitation__en {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    line-height: 1.6;
    color: var(--color-fg-2);
  }

  .tafsir {
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-top: 1px solid var(--color-border-1);
    padding-top: 14px;
  }
  .tafsir__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .tafsir__label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .tafsir__dots {
    display: flex;
    gap: 6px;
  }
  :global(.tafsir__dot) {
    width: 6px;
    height: 6px;
    border-radius: var(--radius-full);
    background: var(--color-border-2);
    cursor: pointer;
    transition: background var(--duration-fast) var(--ease-standard);
  }
  :global(.tafsir__dot.is-active) {
    background: var(--color-accent);
    box-shadow: 0 0 8px var(--color-accent);
  }

  .tafsir__stage {
    position: relative;
    min-height: 110px;
  }
  .tafsir__card {
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 600ms ease;
    pointer-events: none;
  }
  .tafsir__card.active {
    opacity: 1;
    pointer-events: auto;
  }
  .tafsir__meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent);
    margin-bottom: 8px;
    letter-spacing: 0.04em;
  }
  .tafsir__book {
    color: var(--color-accent);
    font-weight: 600;
  }
  .tafsir__author {
    color: var(--color-fg-3);
  }
  .tafsir__text {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    line-height: 1.65;
    color: var(--color-fg-2);
  }
</style>
