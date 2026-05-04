<!--
  App shell. Header carries the Karbala-mosque brand mark + nav, footer
  carries the colophon hint. The corpus pages render their own celestial
  backdrops; the layout stays neutral so the showcase remains legible.
-->
<script lang="ts">
  import '../app.css';
  import type { Snippet } from 'svelte';
  import { Pressable } from '$lib/design-system';
  import { theme } from '$lib/stores';
  import logoDark from '$lib/../static/logo-dark.png';

  let { children }: { children: Snippet } = $props();

  const nav: { label: string; href: string }[] = [
    { label: 'Browse', href: '/' },
    { label: 'Search', href: '/search' },
    { label: 'Qurʾan', href: '/library/sunni-tafsir' },
    { label: 'Hadith', href: '/library/sunni-hadith-general' },
    { label: 'Fiqh', href: '/library/hanafi-fiqh' },
    { label: 'Library', href: '/library' },
  ];
</script>

<div class="shell">
  <header class="shell__header">
    <div class="shell__header-inner">
      <a class="brand" href="/">
        <img class="brand__mark" src={logoDark} alt="Shia Online Library" width="80" height="38" />
        <span class="brand__text">
          <span class="brand__name">Shia Online Library</span>
          <span class="brand__sub">A reading instrument · Sol</span>
        </span>
      </a>

      <nav class="shell__nav" aria-label="Primary">
        {#each nav as n (n.href)}
          <a class="shell__nav-link" href={n.href}>{n.label}</a>
        {/each}
      </nav>

      <Pressable class="shell__theme-toggle" onclick={() => theme.toggle()}>Toggle</Pressable>
    </div>
  </header>

  <main class="shell__main">
    {@render children()}
  </main>

  <footer class="shell__footer">
    <div class="shell__footer-inner">
      <span>Built on the sol-next1 harness</span>
      <span class="shell__footer-sep">·</span>
      <span>design tokens are SSOT</span>
      <span class="shell__footer-sep">·</span>
      <span>raw colors are blocked</span>
    </div>
  </footer>
</div>

<style>
  .shell {
    display: flex;
    min-height: 100vh;
    flex-direction: column;
    position: relative;
    z-index: 1;
  }
  .shell__header {
    position: sticky;
    top: 0;
    z-index: 50;
    border-bottom: 1px solid var(--color-border-1);
    background: color-mix(in oklch, var(--color-bg-0) 70%, transparent);
    backdrop-filter: blur(12px);
  }
  .shell__header-inner {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 32px;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 32px;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: inherit;
  }
  .brand__mark {
    height: 38px;
    width: auto;
    display: block;
    object-fit: contain;
  }
  .brand__text {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }
  .brand__name {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    font-weight: 500;
    color: var(--color-fg-1);
    letter-spacing: var(--tracking-tight);
  }
  .brand__sub {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--color-fg-3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 2px;
  }

  .shell__nav {
    display: flex;
    align-items: center;
    gap: 22px;
    margin-left: auto;
  }
  .shell__nav-link {
    font-family: var(--font-display);
    font-size: var(--text-sm);
    color: var(--color-fg-2);
    text-decoration: none;
    transition: color var(--duration-fast) var(--ease-standard);
  }
  .shell__nav-link:hover {
    color: var(--color-accent);
  }

  :global(.shell__theme-toggle) {
    border: 1px solid var(--color-border-1);
    background: transparent;
    color: var(--color-fg-2);
    padding: 6px 12px;
    border-radius: var(--radius-full);
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    cursor: pointer;
    transition:
      border-color var(--duration-fast) var(--ease-standard),
      color var(--duration-fast) var(--ease-standard);
  }
  :global(.shell__theme-toggle:hover) {
    border-color: var(--color-accent);
    color: var(--color-accent);
  }

  .shell__main {
    flex: 1;
    width: 100%;
  }

  .shell__footer {
    border-top: 1px solid var(--color-border-1);
    background: color-mix(in oklch, var(--color-bg-0) 70%, transparent);
    backdrop-filter: blur(8px);
  }
  .shell__footer-inner {
    max-width: 1280px;
    margin: 0 auto;
    padding: 18px 32px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    text-transform: uppercase;
    letter-spacing: 0.16em;
  }
  .shell__footer-sep {
    color: var(--color-accent);
    opacity: 0.5;
  }

  @media (max-width: 768px) {
    .shell__nav {
      display: none;
    }
    .shell__header-inner {
      padding: 0 20px;
    }
  }
</style>
