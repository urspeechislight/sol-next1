<!--
  Editorial hero — the opening of the home page.

  Composition:
    - Eyebrow line (mono, accent dot)
    - Salawat in Amiri (centred, RTL)
    - Search input with three example "try" chips

  Decorative elements from the design prototype that are intentionally
  deferred to follow-ups:
    - The rotating astrolabe SVG (its own meaningful component)
    - Layered starfield + scholarly grid backdrop
    - Live "now indexing" ticker
    - Manuscript corner cartouches
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { Input, FilterPill } from '$lib/design-system';

  let query = $state('');
  const examples: { q: string; kind: string }[] = [
    { q: 'Ibn Hajar', kind: 'author' },
    { q: 'al-Kafi', kind: 'work' },
    { q: 'Hisham ibn al-Hakam', kind: 'narrator' },
  ];

  function search(q: string) {
    void goto(`/search?q=${encodeURIComponent(q)}`);
  }

  function onEnter(e: KeyboardEvent) {
    if (e.key === 'Enter' && query.trim()) search(query.trim());
  }
</script>

<section class="hero" aria-label="Hero">
  <div class="hero__inner">
    <div class="hero__eyebrow">
      <span class="hero__eyebrow-mark" aria-hidden="true"></span>
      <span>Sol &middot; A reading instrument for the Islamic textual tradition</span>
    </div>

    <div class="hero__salawat" dir="rtl" aria-label="Salawat">
      <div class="hero__salawat-main">اللهم صل على محمد وآل محمد</div>
      <div class="hero__salawat-ext">وعجل فرجهم والعن أعداءهم</div>
    </div>

    <div class="hero__search">
      <Input
        size="lg"
        placeholder="Search authors, titles, narrators, ḥadīth…"
        bind:value={query}
        onkeydown={onEnter}
      />
      <div class="hero__chips">
        <span class="hero__chips-label">Try</span>
        {#each examples as c (c.q)}
          <FilterPill onclick={() => search(c.q)}>
            <span class="hero__chip-kind">{c.kind}</span>
            <span>{c.q}</span>
          </FilterPill>
        {/each}
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    position: relative;
    padding: 64px 0 32px;
  }
  .hero__inner {
    max-width: 720px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }

  .hero__eyebrow {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-fg-3);
    letter-spacing: var(--tracking-wide);
    text-transform: uppercase;
  }
  .hero__eyebrow-mark {
    width: 6px;
    height: 6px;
    border-radius: var(--radius-full);
    background: var(--color-accent);
    box-shadow: var(--shadow-glow-accent);
  }

  .hero__salawat {
    text-align: center;
    font-family: var(--font-arabic);
    color: var(--color-fg-1);
    line-height: 1.3;
  }
  .hero__salawat-main {
    font-size: var(--text-4xl);
    font-weight: 700;
    letter-spacing: 0.02em;
  }
  .hero__salawat-ext {
    font-size: var(--text-xl);
    color: var(--color-fg-2);
    margin-top: 8px;
    font-weight: 400;
  }

  .hero__search {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .hero__chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
  }
  .hero__chips-label {
    color: var(--color-fg-3);
    letter-spacing: var(--tracking-wide);
    text-transform: uppercase;
    margin-right: 4px;
  }
  .hero__chip-kind {
    color: var(--color-accent);
    text-transform: uppercase;
    letter-spacing: var(--tracking-wide);
    font-size: 10px;
    margin-right: 6px;
  }
</style>
