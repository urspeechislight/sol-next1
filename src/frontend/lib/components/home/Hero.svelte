<!--
  Editorial hero — the opening of the home page.

  Composition:
    - LEFT column: editorial eyebrow, salawat in Amiri, search +
      example chips, live "now indexing" ticker
    - RIGHT column: the rotating Astrolabe centerpiece
    - Manuscript corner cartouches at the four corners

  Below 980px the columns stack and the astrolabe sits beneath the
  copy. Below 640px the astrolabe is hidden (it doesn't read at small
  sizes and the cabinet is the primary nav anyway).
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { Input, FilterPill } from '$lib/design-system';
  import { BOOKS } from '$lib/fixtures';
  import Astrolabe from './Astrolabe.svelte';
  import Cornerpiece from './Cornerpiece.svelte';
  import LiveTicker from './LiveTicker.svelte';

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
  <Cornerpiece pos="tl" />
  <Cornerpiece pos="tr" />
  <Cornerpiece pos="bl" />
  <Cornerpiece pos="br" />

  <div class="hero__inner">
    <div class="hero__copy">
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

      <LiveTicker books={BOOKS} />
    </div>

    <div class="hero__astrolabe">
      <Astrolabe />
    </div>
  </div>
</section>

<style>
  .hero {
    position: relative;
    padding: 80px 32px 48px;
    max-width: 1280px;
    margin-inline: auto;
  }

  .hero__inner {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 48px;
    align-items: center;
  }

  .hero__copy {
    display: flex;
    flex-direction: column;
    gap: 28px;
    min-width: 0;
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

  .hero__astrolabe {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 40px;
  }

  @media (max-width: 980px) {
    .hero__inner {
      grid-template-columns: 1fr;
      gap: 56px;
    }
    .hero__copy {
      max-width: 720px;
      margin-inline: auto;
    }
    .hero__astrolabe {
      max-width: 420px;
      margin-inline: auto;
    }
  }
  @media (max-width: 640px) {
    .hero {
      padding: 56px 20px 32px;
    }
    .hero__astrolabe {
      display: none;
    }
    .hero__salawat-main {
      font-size: var(--text-3xl);
    }
  }
</style>
