<!--
  Folio panel — book of the day rendered as a slowly-cycling vitrine:
  cover face → spine → open-page (every 4.5s). Like a museum display.
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { Pressable } from '$lib/design-system';
  import type { Book, BookOfDay } from '$lib/fixtures';

  interface Props {
    book: Book;
    daily: BookOfDay;
  }
  let { book, daily }: Props = $props();

  // Faces: cover, spine, page. Cycle every 4.5s.
  const faces = ['cover', 'spine', 'page'] as const;
  const FACE_MS = 4500;
  let faceIdx = $state(0);
  $effect(() => {
    const id = setInterval(() => {
      faceIdx = (faceIdx + 1) % faces.length;
    }, FACE_MS);
    return () => clearInterval(id);
  });
  const face = $derived(faces[faceIdx]);

  function openReader() {
    void goto(`/reader/${book.urn}/${daily.openTo.page}`);
  }
</script>

<article class="panel">
  <div class="panel__eyebrow">
    <span class="panel__eyebrow-num">III</span>
    <span class="panel__eyebrow-label">Folio</span>
    <span class="panel__eyebrow-live" aria-hidden="true"></span>
    <span class="panel__eyebrow-sub">Book of the Day</span>
  </div>

  <h3 class="panel__title">
    <em>Open</em> the codex
  </h3>

  <Pressable class="folio" onclick={openReader} title="Open the reader">
    <div class="folio__stage">
      <div class="folio__face folio__face--cover" class:active={face === 'cover'}>
        <div class="folio__cover-spine"></div>
        <div class="folio__cover-frame">
          <span class="folio__cover-arabic" dir="rtl">{book.titleAr}</span>
          <span class="folio__cover-divider"></span>
          <span class="folio__cover-en">{book.titleEn}</span>
          <span class="folio__cover-author">{book.author}</span>
        </div>
      </div>
      <div class="folio__face folio__face--spine" class:active={face === 'spine'}>
        <div class="folio__spine-text" dir="rtl">{book.titleAr}</div>
      </div>
      <div class="folio__face folio__face--page" class:active={face === 'page'}>
        <div class="folio__page-chapter" dir="rtl">{daily.openTo.chapterEn}</div>
        <div class="folio__page-rule"></div>
        <div class="folio__page-body">
          <p>{book.blurb}</p>
        </div>
        <div class="folio__page-num">p. {daily.openTo.page}</div>
      </div>
    </div>
  </Pressable>

  <div class="folio__caption">
    <p class="folio__rationale">{daily.rationale}</p>
    <div class="folio__cta">
      <span class="folio__cta-arrow">→</span>
      Open to <em>{daily.openTo.chapterEn}</em>
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
    font-family: var(--font-display);
    font-size: var(--text-2xl);
    color: var(--color-fg-1);
    letter-spacing: var(--tracking-tight);
    font-weight: 500;
  }
  .panel__title em {
    font-style: italic;
    color: var(--color-accent);
    font-weight: 400;
  }

  :global(.folio) {
    display: block;
    width: 100%;
    cursor: pointer;
    border: none;
    background: transparent;
    padding: 0;
  }
  .folio__stage {
    position: relative;
    aspect-ratio: 3 / 4;
    width: 100%;
    max-width: 220px;
    margin-inline: auto;
    border-radius: var(--radius-sm);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    background: var(--color-bg-2);
  }
  .folio__face {
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 700ms ease;
    display: flex;
    flex-direction: column;
  }
  .folio__face.active {
    opacity: 1;
  }

  /* COVER */
  .folio__face--cover {
    background:
      radial-gradient(ellipse at 50% 0%, var(--color-accent-soft), transparent 70%),
      linear-gradient(180deg, var(--color-bg-night-1) 0%, var(--color-bg-night-2) 100%);
    padding: 28px 18px 18px;
    align-items: center;
    text-align: center;
    color: var(--color-fg-1);
  }
  .folio__cover-spine {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 8px;
    background: linear-gradient(to right, var(--color-crimson) 0%, transparent 100%);
    opacity: 0.5;
  }
  .folio__cover-frame {
    border: 1px solid var(--color-accent);
    padding: 22px 14px;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
  }
  .folio__cover-arabic {
    font-family: var(--font-arabic);
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--color-fg-1);
    line-height: 1.2;
  }
  .folio__cover-divider {
    width: 30px;
    height: 1px;
    background: var(--color-accent);
  }
  .folio__cover-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-accent);
  }
  .folio__cover-author {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--color-fg-3);
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  /* SPINE */
  .folio__face--spine {
    background: linear-gradient(90deg, var(--color-crimson) 0%, var(--color-bg-2) 100%);
    align-items: center;
    justify-content: center;
  }
  .folio__spine-text {
    font-family: var(--font-arabic);
    font-size: var(--text-3xl);
    font-weight: 700;
    color: var(--color-fg-1);
    writing-mode: vertical-rl;
    text-orientation: mixed;
  }

  /* PAGE */
  .folio__face--page {
    background: linear-gradient(180deg, var(--color-vellum) 0%, var(--color-vellum) 100%);
    color: var(--color-bg-0);
    padding: 16px 18px;
    gap: 8px;
  }
  .folio__page-chapter {
    font-family: var(--font-arabic);
    font-size: var(--text-base);
    font-weight: 700;
    color: var(--color-bg-0);
    text-align: center;
  }
  .folio__page-rule {
    height: 1px;
    background: var(--color-bg-0);
    opacity: 0.3;
    margin: 4px 0;
  }
  .folio__page-body p {
    margin: 0;
    font-family: var(--font-display);
    font-size: 11px;
    line-height: 1.45;
    color: var(--color-bg-0);
    opacity: 0.7;
    flex: 1;
  }
  .folio__page-num {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--color-bg-0);
    opacity: 0.5;
    text-align: center;
    letter-spacing: 0.18em;
  }

  .folio__caption {
    display: flex;
    flex-direction: column;
    gap: 8px;
    border-top: 1px solid var(--color-border-1);
    padding-top: 12px;
  }
  .folio__rationale {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    line-height: 1.55;
    color: var(--color-fg-2);
  }
  .folio__cta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--color-accent);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .folio__cta em {
    font-family: var(--font-display);
    font-style: italic;
    color: var(--color-fg-1);
    text-transform: none;
    letter-spacing: 0;
    font-size: var(--text-sm);
  }
  .folio__cta-arrow {
    color: var(--color-accent);
  }
</style>
