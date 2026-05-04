<!--
  Table-of-contents sidebar — left rail in the reader. Click any
  chapter to jump to its page.
-->
<script lang="ts">
  import { Pressable } from '$lib/design-system';
  import type { TocItem } from '$lib/fixtures';

  interface Props {
    items: TocItem[];
    pageNum: number;
    onJump: (page: number) => void;
  }
  let { items, pageNum, onJump }: Props = $props();

  function activeIdx(items: TocItem[], p: number): number {
    let best = 0;
    for (let i = 0; i < items.length; i++) {
      const it = items[i];
      if (it && it.page <= p) best = i;
    }
    return best;
  }
  const active = $derived(activeIdx(items, pageNum));
</script>

<aside class="toc">
  <div class="toc__head">
    <span class="toc__eyebrow">Contents</span>
    <span dir="rtl" class="toc__eyebrow-ar">المحتويات</span>
  </div>

  <ol class="toc__list">
    {#each items as it, i (it.page)}
      <li class="toc__item">
        <Pressable
          class="toc__btn {i === active ? 'is-active' : ''}"
          onclick={() => onJump(it.page)}
        >
          <span class="toc__num">{String(i + 1).padStart(2, '0')}</span>
          <span class="toc__titles">
            <span class="toc__ar" dir="rtl">{it.title}</span>
            <span class="toc__en">{it.titleEn}</span>
          </span>
          <span class="toc__page">p. {it.page}</span>
        </Pressable>
      </li>
    {/each}
  </ol>
</aside>

<style>
  .toc {
    border-right: 1px solid var(--reader-rule);
    padding: 28px 18px;
    overflow-y: auto;
    background: color-mix(in oklch, var(--reader-bg) 96%, var(--color-accent) 4%);
  }
  .toc__head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-bottom: 12px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--reader-rule);
  }
  .toc__eyebrow {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.6;
  }
  .toc__eyebrow-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    opacity: 0.75;
    color: var(--reader-honorific);
  }
  .toc__list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  :global(.toc__btn) {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: baseline;
    gap: 10px;
    width: 100%;
    text-align: left;
    padding: 10px 8px;
    border: none;
    background: transparent;
    color: inherit;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background var(--duration-fast) var(--ease-standard);
  }
  :global(.toc__btn:hover) {
    background: var(--reader-quote-bg);
  }
  :global(.toc__btn.is-active) {
    background: var(--color-accent-soft);
  }
  .toc__num {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.18em;
    opacity: 0.55;
  }
  .toc__titles {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }
  .toc__ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    line-height: 1.4;
    font-weight: 600;
    color: var(--reader-honorific);
  }
  .toc__en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 12px;
    line-height: 1.3;
    opacity: 0.75;
  }
  .toc__page {
    font-family: var(--font-mono);
    font-size: 10px;
    opacity: 0.55;
    letter-spacing: 0.1em;
  }
</style>
