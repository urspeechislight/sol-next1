<!--
  Reader toolbar — three rows: context strip, pagination, settings.
-->
<script lang="ts">
  import { Pressable, Input } from '$lib/design-system';
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
    bookSearch: string;
    onTheme: (t: 'bright' | 'dark' | 'classical') => void;
    onLang: (l: 'ar' | 'both' | 'en') => void;
    onFontSize: (n: number) => void;
    onToggleToc: () => void;
    onToggleIsnad: () => void;
    onNav: (page: number) => void;
    onBookSearch: (q: string) => void;
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
    bookSearch,
    onTheme,
    onLang,
    onFontSize,
    onToggleToc,
    onToggleIsnad,
    onNav,
    onBookSearch,
  }: Props = $props();

  // Page-jump: indicator becomes editable on click.
  let jumping = $state(false);
  let jumpInput = $state('');
  function startJump() {
    jumpInput = String(pageNum);
    jumping = true;
  }
  function commitJump() {
    const n = parseInt(jumpInput, 10);
    if (!Number.isNaN(n) && n >= 1) onNav(Math.min(n, totalPages));
    jumping = false;
  }
  function jumpKey(e: KeyboardEvent) {
    if (e.key === 'Enter') commitJump();
    if (e.key === 'Escape') jumping = false;
  }

  // Search-in-book inline field.
  let searchOpen = $state(false);
  let searchQ = $state('');
  $effect(() => {
    searchQ = bookSearch;
  });
  function toggleSearch() {
    searchOpen = !searchOpen;
    if (!searchOpen) {
      searchQ = '';
      onBookSearch('');
    }
  }
  function searchKey(e: KeyboardEvent) {
    if (e.key === 'Enter') onBookSearch(searchQ);
    if (e.key === 'Escape') {
      searchOpen = false;
      searchQ = '';
      onBookSearch('');
    }
  }

  // Svelte action: focus the inner text field of a wrapper element on
  // mount. Avoids a11y_autofocus while keeping the same UX (the user
  // just clicked the field's container so focus is intentional).
  function wrapFocus(node: HTMLElement) {
    queueMicrotask(() => {
      const field = node.querySelector('input');
      field?.focus();
      field?.select();
    });
  }

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
    {#if jumping}
      <span class="rt__page rt__page--edit" use:wrapFocus>
        <Input
          size="sm"
          inputmode="numeric"
          bind:value={jumpInput}
          onkeydown={jumpKey}
          onblur={commitJump}
          aria-label="Jump to page"
          class="rt__page-input"
        />
        <span class="rt__page-sep">/</span>
        <span class="rt__page-tot">{totalPages.toLocaleString()}</span>
      </span>
    {:else}
      <Pressable class="rt__page" onclick={startJump} aria-label="Jump to page">
        <span class="rt__page-n">{pageNum.toLocaleString()}</span>
        <span class="rt__page-sep">/</span>
        <span class="rt__page-tot">{totalPages.toLocaleString()}</span>
      </Pressable>
    {/if}
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

    <Pressable class="rt__pill {searchOpen ? 'is-active' : ''}" onclick={toggleSearch}>
      ⌕ {searchOpen ? 'Close search' : 'Search book'}
    </Pressable>
    <Pressable class="rt__pill {tocOpen ? 'is-active' : ''}" onclick={onToggleToc}
      >Contents</Pressable
    >
    <Pressable class="rt__pill {isnadOpen ? 'is-active' : ''}" onclick={onToggleIsnad}
      >Isnād</Pressable
    >
  </div>

  {#if searchOpen}
    <div class="rt__row rt__row--search">
      <Input
        size="sm"
        bind:value={searchQ}
        onkeydown={searchKey}
        placeholder="Search this book — Arabic or English…"
      />
      <Pressable class="rt__pill" onclick={() => onBookSearch(searchQ)}>Find</Pressable>
      {#if bookSearch}
        <span class="rt__search-info">Highlighting: <em>{bookSearch}</em></span>
      {/if}
    </div>
  {/if}
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

  :global(.rt__page) {
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: var(--text-base);
    padding: 4px 14px;
    border-radius: var(--radius-full);
    border: 1px solid var(--reader-rule);
    background: transparent;
    color: inherit;
    cursor: pointer;
  }
  :global(.rt__page:hover) {
    border-color: var(--color-accent);
  }
  .rt__page--edit {
    cursor: text;
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
  :global(.rt__page-input) {
    width: 64px;
    background: transparent;
    border: none;
    text-align: right;
    font-weight: 600;
    height: auto;
    padding: 0;
    color: inherit;
  }

  .rt__row--search {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .rt__row--search :global(input) {
    flex: 1;
    background: transparent;
    color: inherit;
    border-color: var(--reader-rule);
  }
  .rt__search-info {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--reader-honorific);
    letter-spacing: 0.1em;
  }
  .rt__search-info em {
    font-family: var(--font-display);
    font-style: italic;
    color: var(--color-accent);
    text-transform: none;
    letter-spacing: 0;
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
