<!--
  Reader toolbar — three rows: context strip, pagination, settings.
-->
<script lang="ts">
  import { Pressable } from '$lib/design-system';
  import type { Book } from '$lib/fixtures';

  interface Props {
    book: Book;
    pageNum: number;
    totalPages: number;
    theme: 'bright' | 'dark' | 'classical';
    langMode: 'ar' | 'both' | 'en';
    fontSize: number;
    tocOpen: boolean;
    isnadOpen: boolean;
    onTheme: (t: 'bright' | 'dark' | 'classical') => void;
    onLang: (l: 'ar' | 'both' | 'en') => void;
    onFontSize: (n: number) => void;
    onToggleToc: () => void;
    onToggleIsnad: () => void;
    onNav: (page: number) => void;
  }
  let {
    book,
    pageNum,
    totalPages,
    theme,
    langMode,
    fontSize,
    tocOpen,
    isnadOpen,
    onTheme,
    onLang,
    onFontSize,
    onToggleToc,
    onToggleIsnad,
    onNav,
  }: Props = $props();

  const themes: { v: typeof theme; l: string }[] = [
    { v: 'bright', l: 'Bright' },
    { v: 'dark', l: 'Dark' },
    { v: 'classical', l: 'Classical' },
  ];
  const langs: { v: typeof langMode; l: string }[] = [
    { v: 'ar', l: 'AR' },
    { v: 'both', l: 'AR · EN' },
    { v: 'en', l: 'EN' },
  ];
</script>

<header class="rt">
  <div class="rt__row rt__row--ctx">
    <a class="rt__back" href={`/library/${book.category}`}>← Library</a>
    <span class="rt__sep" aria-hidden="true"></span>
    <span class="rt__title-ar" dir="rtl">{book.titleAr}</span>
    <span class="rt__title-en">· {book.titleEn}</span>
    <span class="rt__author">· {book.author}</span>
    <span class="rt__urn">urn:{book.urn}</span>
  </div>

  <div class="rt__row rt__row--pag">
    <Pressable
      class="rt__pill"
      onclick={() => onNav(Math.max(1, pageNum - 1))}
      aria-label="Previous page">‹</Pressable
    >
    <span class="rt__page">
      <span class="rt__page-n">{pageNum.toLocaleString()}</span>
      <span class="rt__page-sep">/</span>
      <span class="rt__page-tot">{totalPages.toLocaleString()}</span>
    </span>
    <Pressable class="rt__pill" onclick={() => onNav(pageNum + 1)} aria-label="Next page"
      >›</Pressable
    >
  </div>

  <div class="rt__row rt__row--set">
    <div class="rt__seg">
      {#each themes as t (t.v)}
        <Pressable
          class="rt__seg-btn {theme === t.v ? 'is-active' : ''}"
          onclick={() => onTheme(t.v)}>{t.l}</Pressable
        >
      {/each}
    </div>

    <div class="rt__seg">
      <Pressable class="rt__seg-btn" onclick={() => onFontSize(fontSize - 2)} aria-label="Smaller"
        >−</Pressable
      >
      <span class="rt__fs">{fontSize}px</span>
      <Pressable class="rt__seg-btn" onclick={() => onFontSize(fontSize + 2)} aria-label="Larger"
        >+</Pressable
      >
    </div>

    <div class="rt__seg">
      {#each langs as l (l.v)}
        <Pressable
          class="rt__seg-btn {langMode === l.v ? 'is-active' : ''}"
          onclick={() => onLang(l.v)}>{l.l}</Pressable
        >
      {/each}
    </div>

    <Pressable class="rt__pill {tocOpen ? 'is-active' : ''}" onclick={onToggleToc}
      >Contents</Pressable
    >
    <Pressable class="rt__pill {isnadOpen ? 'is-active' : ''}" onclick={onToggleIsnad}
      >Isnād</Pressable
    >
  </div>
</header>

<style>
  .rt {
    background: var(--reader-toolbar-bg);
    color: var(--reader-toolbar-fg);
    border-bottom: 1px solid var(--reader-rule);
    position: sticky;
    top: 0;
    z-index: 50;
  }
  .rt__row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 24px;
    border-bottom: 1px solid var(--reader-rule);
  }
  .rt__row:last-child {
    border-bottom: none;
  }
  .rt__row--pag {
    justify-content: center;
  }
  .rt__row--set {
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .rt__back {
    text-decoration: none;
    color: inherit;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    opacity: 0.7;
  }
  .rt__back:hover {
    opacity: 1;
  }
  .rt__sep {
    width: 1px;
    height: 16px;
    background: var(--reader-rule);
  }
  .rt__title-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-lg);
    font-weight: 700;
  }
  .rt__title-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    opacity: 0.75;
  }
  .rt__author {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    opacity: 0.55;
  }
  .rt__urn {
    margin-left: auto;
    font-family: var(--font-mono);
    font-size: 10px;
    opacity: 0.55;
    letter-spacing: 0.1em;
  }

  :global(.rt__pill) {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: var(--radius-full);
    border: 1px solid var(--reader-rule);
    background: transparent;
    color: inherit;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    cursor: pointer;
    transition: background var(--duration-fast) var(--ease-standard);
  }
  :global(.rt__pill:hover),
  :global(.rt__pill.is-active) {
    background: var(--color-accent-soft);
    border-color: var(--color-accent);
  }

  .rt__page {
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: var(--text-base);
  }
  .rt__page-n {
    font-weight: 600;
  }
  .rt__page-sep {
    opacity: 0.4;
  }
  .rt__page-tot {
    opacity: 0.65;
    font-size: var(--text-sm);
  }

  .rt__seg {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--reader-rule);
    border-radius: var(--radius-full);
    padding: 2px;
    gap: 2px;
  }
  :global(.rt__seg-btn) {
    background: transparent;
    border: none;
    padding: 4px 12px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    cursor: pointer;
    color: inherit;
    border-radius: var(--radius-full);
    transition: background var(--duration-fast) var(--ease-standard);
  }
  :global(.rt__seg-btn:hover) {
    background: var(--color-accent-soft);
  }
  :global(.rt__seg-btn.is-active) {
    background: var(--color-accent);
    color: var(--color-fg-on-accent);
  }
  .rt__fs {
    padding: 0 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    opacity: 0.7;
  }
</style>
