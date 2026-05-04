<!--
  Reader — full-screen takeover. Toolbar + collapsible TOC sidebar +
  main page view + collapsible isnad sidebar. The page fixture uses
  the al-Kafi Kitab al-Tawhid sample regardless of the urn so the
  visual is realistic; backend wiring will swap that for real data.
-->
<script lang="ts">
  import { page } from '$app/state';
  import { goto } from '$app/navigation';
  import { findBook, BOOKS, SAMPLE_TOC, SAMPLE_PAGE } from '$lib/fixtures';
  import Toolbar from '$lib/components/reader/Toolbar.svelte';
  import TocSidebar from '$lib/components/reader/TocSidebar.svelte';
  import PageView from '$lib/components/reader/PageView.svelte';
  import IsnadSidebar from '$lib/components/reader/IsnadSidebar.svelte';

  const urn = $derived(String(page.params.urn ?? ''));
  const pageNum = $derived(parseInt(String(page.params.pageNum ?? '109'), 10) || 109);

  const book = $derived(findBook(urn) ?? BOOKS[2]!);

  // Reader settings — per-session, no persistence yet.
  let theme = $state<'bright' | 'dark' | 'classical'>('classical');
  let langMode = $state<'ar' | 'both' | 'en'>('both');
  let fontSize = $state(20);

  let tocOpen = $state(true);
  let isnadOpen = $state(true);
  let activeIsnad = $state(0);

  function navTo(p: number) {
    void goto(`/reader/${urn}/${p}`);
  }

  const totalPages = $derived(book.pageCount);
  const activeHadith = $derived(SAMPLE_PAGE.hadiths[activeIsnad] ?? SAMPLE_PAGE.hadiths[0]!);
</script>

<svelte:head>
  <title>{book.titleEn} · p. {pageNum} · Reader</title>
</svelte:head>

<div class="reader" data-reader-theme={theme}>
  <Toolbar
    {book}
    {pageNum}
    {totalPages}
    {theme}
    {langMode}
    {fontSize}
    {tocOpen}
    {isnadOpen}
    onTheme={(t: 'bright' | 'dark' | 'classical') => (theme = t)}
    onLang={(l: 'ar' | 'both' | 'en') => (langMode = l)}
    onFontSize={(n: number) => (fontSize = Math.max(14, Math.min(28, n)))}
    onToggleToc={() => (tocOpen = !tocOpen)}
    onToggleIsnad={() => (isnadOpen = !isnadOpen)}
    onNav={navTo}
  />

  <div class="reader__layout">
    {#if tocOpen}
      <TocSidebar items={SAMPLE_TOC} {pageNum} onJump={navTo} />
    {/if}

    <main class="reader__main">
      <PageView
        page={SAMPLE_PAGE}
        {langMode}
        {fontSize}
        {activeIsnad}
        onActivate={(i: number) => (activeIsnad = i)}
      />
    </main>

    {#if isnadOpen}
      <IsnadSidebar hadith={activeHadith} />
    {/if}
  </div>
</div>

<style>
  .reader {
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--color-bg-0);
    color: var(--color-fg-1);
  }

  /* Reader themes — values come from tokens.css. */
  .reader[data-reader-theme='classical'] {
    --reader-bg: var(--reader-classical-bg);
    --reader-fg: var(--reader-classical-fg);
    --reader-rule: var(--reader-classical-rule);
    --reader-honorific: var(--reader-classical-honorific);
    --reader-quote-bg: var(--reader-classical-quote-bg);
    --reader-toolbar-bg: var(--reader-classical-toolbar-bg);
    --reader-toolbar-fg: var(--reader-classical-fg);
  }
  .reader[data-reader-theme='bright'] {
    --reader-bg: var(--reader-bright-bg);
    --reader-fg: var(--reader-bright-fg);
    --reader-rule: var(--reader-bright-rule);
    --reader-honorific: var(--color-accent-strong);
    --reader-quote-bg: var(--reader-bright-quote-bg);
    --reader-toolbar-bg: var(--reader-bright-toolbar-bg);
    --reader-toolbar-fg: var(--reader-bright-fg);
  }
  .reader[data-reader-theme='dark'] {
    --reader-bg: var(--color-bg-0);
    --reader-fg: var(--color-fg-1);
    --reader-rule: var(--color-border-1);
    --reader-honorific: var(--color-accent);
    --reader-quote-bg: var(--color-bg-1);
    --reader-toolbar-bg: var(--color-bg-1);
    --reader-toolbar-fg: var(--color-fg-1);
  }

  .reader[data-reader-theme] {
    background: var(--reader-bg);
    color: var(--reader-fg);
  }

  .reader__layout {
    flex: 1;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    overflow: hidden;
  }
  /* The .toc / .isnad classes live inside child components, so :has must
     be :global-aware. */
  .reader__layout:global(:has(.toc)):not(:global(:has(.isnad))) {
    grid-template-columns: 280px minmax(0, 1fr);
  }
  .reader__layout:global(:has(.isnad)):not(:global(:has(.toc))) {
    grid-template-columns: minmax(0, 1fr) 320px;
  }
  .reader__layout:global(:has(.toc)):global(:has(.isnad)) {
    grid-template-columns: 280px minmax(0, 1fr) 320px;
  }
  .reader__main {
    overflow-y: auto;
    padding: 48px 32px 80px;
  }

  @media (max-width: 1024px) {
    .reader__layout {
      grid-template-columns: minmax(0, 1fr) !important;
    }
    :global(.reader .toc),
    :global(.reader .isnad) {
      display: none;
    }
  }
</style>
