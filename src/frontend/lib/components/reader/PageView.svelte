<!--
  Reader page view — the main column. Header (page number, chapter,
  section), then a HadithBlock for each hadith. Footnotes at the end.
-->
<script lang="ts">
  import { Pressable } from '$lib/design-system';
  import type { BookPage } from '$lib/fixtures';

  interface Props {
    page: BookPage;
    langMode: 'ar' | 'both' | 'en';
    fontSize: number;
    activeIsnad: number;
    onActivate: (i: number) => void;
  }
  let { page, langMode, fontSize, activeIsnad, onActivate }: Props = $props();

  const showAr = $derived(langMode === 'ar' || langMode === 'both');
  const showEn = $derived(langMode === 'en' || langMode === 'both');
  const grid = $derived(langMode === 'both');

  const eastDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  function arabicDigit(n: number): string {
    return String(n)
      .split('')
      .map((d) => eastDigits[parseInt(d, 10)] ?? d)
      .join('');
  }
</script>

<article class="pv" style:--reader-fs="{fontSize}px">
  <header class="pv__head">
    <div class="pv__head-meta">Page {page.pageNumber} · {page.sectionTitleEn}</div>
    <h2 class="pv__head-chapter" dir="rtl">{page.chapterTitle}</h2>
    <div class="pv__head-section" dir="rtl">{page.sectionTitle}</div>
    <div class="pv__head-en">{page.chapterTitleEn} · {page.sectionTitleEn}</div>
  </header>

  {#each page.hadiths as h, i (h.n)}
    <Pressable class="hb {i === activeIsnad ? 'is-active' : ''}" onclick={() => onActivate(i)}>
      <div class="hb__head">
        <div class="hb__id">
          <span class="hb__num" aria-hidden="true">{arabicDigit(h.n)}</span>
          <span class="hb__label">Hadith {h.n} · {h.narrators.length} narrators</span>
        </div>
        <span class="hb__grade">
          <span class="hb__grade-dot" aria-hidden="true"></span>
          ṣaḥīḥ
        </span>
      </div>

      {#if showAr}
        <div class="hb__isnad" dir="rtl">{h.isnadAr}</div>
      {:else if showEn}
        <div class="hb__isnad-en">
          Chain: {h.narrators.map((n) => n.name).join(' ← ')}, from Abū ʿAbdillah al-Ṣādiq
        </div>
      {/if}

      <div class="hb__matn" class:grid>
        {#if showAr}
          <p class="hb__matn-ar" dir="rtl">{h.matnAr}</p>
        {/if}
        {#if showEn}
          <p class="hb__matn-en">{h.matnEn}</p>
        {/if}
      </div>

      {#if h.crossRefs.length}
        <div class="hb__refs">
          <span class="hb__refs-label">Parallels</span>
          {#each h.crossRefs as r, ri (ri)}
            <span class="hb__ref">
              <span class="hb__ref-ar" dir="rtl">{r.bookAr}</span>
              <span class="hb__ref-en">{r.book}</span>
              <span class="hb__ref-page">p. {r.page}</span>
            </span>
          {/each}
        </div>
      {/if}
    </Pressable>
  {/each}

  <footer class="pv__foot">
    <div class="pv__foot-label">Footnotes</div>
    <div class="pv__foot-body" dir="rtl">
      (١) في نسخة "ج": وَأَثْبَتَتْهُ الْعُقُولُ بِالْفِكْرَةِ، وذكره الصدوق في التوحيد ص ١٠٨.
    </div>
  </footer>
</article>

<style>
  .pv {
    max-width: 920px;
    margin: 0 auto;
  }

  .pv__head {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--reader-rule);
  }
  .pv__head-meta {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    opacity: 0.55;
    margin-bottom: 10px;
  }
  .pv__head-chapter {
    margin: 0 0 6px;
    font-family: var(--font-arabic);
    font-size: clamp(1.75rem, 3vw, 2.25rem);
    font-weight: 600;
    line-height: 1.3;
    color: var(--reader-honorific);
  }
  .pv__head-section {
    font-family: var(--font-arabic);
    font-size: var(--text-lg);
    opacity: 0.75;
  }
  .pv__head-en {
    margin-top: 6px;
    font-family: var(--font-display);
    font-style: italic;
    font-size: 13px;
    opacity: 0.65;
  }

  :global(.hb) {
    display: block;
    width: 100%;
    text-align: inherit;
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius-lg);
    padding: 22px;
    margin-bottom: 22px;
    cursor: pointer;
    color: inherit;
    transition:
      background var(--duration-normal) var(--ease-standard),
      border-color var(--duration-normal) var(--ease-standard);
  }
  :global(.hb:hover) {
    border-color: var(--reader-rule);
  }
  :global(.hb.is-active) {
    background: var(--reader-quote-bg);
    border-color: var(--reader-rule);
  }

  .hb__head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }
  .hb__id {
    display: inline-flex;
    align-items: center;
    gap: 10px;
  }
  .hb__num {
    width: 32px;
    height: 32px;
    border-radius: var(--radius-full);
    background: var(--reader-honorific);
    color: var(--reader-bg);
    font-family: var(--font-arabic);
    font-weight: 700;
    font-size: var(--text-base);
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .hb__label {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.6;
  }
  .hb__grade {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: var(--radius-full);
    background: var(--color-success-soft);
    color: var(--color-success);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .hb__grade-dot {
    width: 6px;
    height: 6px;
    border-radius: var(--radius-full);
    background: currentColor;
  }

  .hb__isnad {
    font-family: var(--font-arabic);
    font-size: calc(var(--reader-fs) - 2px);
    line-height: 2;
    color: var(--reader-honorific);
    font-weight: 500;
    padding-bottom: 14px;
    margin-bottom: 16px;
    border-bottom: 1px dashed var(--reader-rule);
  }
  .hb__isnad-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    opacity: 0.75;
    line-height: 1.7;
    padding-bottom: 14px;
    margin-bottom: 16px;
    border-bottom: 1px dashed var(--reader-rule);
  }

  .hb__matn.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }
  .hb__matn-ar {
    margin: 0;
    font-family: var(--font-arabic);
    font-size: var(--reader-fs);
    line-height: 2.05;
    color: var(--reader-fg);
    text-align: justify;
  }
  .hb__matn-en {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(var(--reader-fs) - 4px);
    line-height: 1.7;
    color: var(--reader-fg);
    opacity: 0.85;
    font-style: italic;
  }

  .hb__refs {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px dashed var(--reader-rule);
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.7;
  }
  .hb__refs-label {
    color: var(--reader-honorific);
  }
  .hb__ref {
    display: inline-flex;
    align-items: baseline;
    gap: 6px;
  }
  .hb__ref-ar {
    font-family: var(--font-arabic);
    font-size: 12px;
    text-transform: none;
    letter-spacing: 0;
    color: var(--reader-honorific);
  }
  .hb__ref-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 12px;
    text-transform: none;
    letter-spacing: 0;
  }
  .hb__ref-page {
    opacity: 0.6;
  }

  .pv__foot {
    margin-top: 56px;
    padding-top: 24px;
    border-top: 1px solid var(--reader-rule);
  }
  .pv__foot-label {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.55;
    margin-bottom: 12px;
  }
  .pv__foot-body {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    line-height: 1.9;
    opacity: 0.78;
  }
</style>
