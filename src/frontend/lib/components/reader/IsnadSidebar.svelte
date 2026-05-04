<!--
  Isnad sidebar — right rail. Renders the active hadith's narrator
  chain as a vertical list with reliability grades, plus a vertical
  SVG visualization showing the chain links.
-->
<script lang="ts">
  import { Pressable } from '$lib/design-system';
  import type { Hadith } from '$lib/fixtures';

  interface Props {
    hadith: Hadith;
  }
  let { hadith }: Props = $props();

  type Viz = 'tree' | 'flow' | 'cards';
  let viz = $state<Viz>('tree');
  const vizOptions: { v: Viz; l: string }[] = [
    { v: 'tree', l: 'Tree' },
    { v: 'flow', l: 'Flow' },
    { v: 'cards', l: 'Cards' },
  ];
</script>

<aside class="isnad">
  <div class="isnad__head">
    <span class="isnad__eyebrow">Isnād</span>
    <span dir="rtl" class="isnad__eyebrow-ar">الإسناد</span>
  </div>

  <div class="isnad__viz-toggle" role="tablist" aria-label="Isnad visualization">
    {#each vizOptions as o (o.v)}
      <Pressable class="isnad__viz-btn {viz === o.v ? 'is-active' : ''}" onclick={() => (viz = o.v)}
        >{o.l}</Pressable
      >
    {/each}
  </div>

  <p class="isnad__intro">
    Chain of <em>{hadith.narrators.length}</em> narrators transmitting hadith №{hadith.n}.
  </p>

  {#if viz === 'tree'}
    <ol class="isnad__list">
      {#each hadith.narrators as n, i (i)}
        <li class="isnad__hop">
          <span class="isnad__hop-mark" aria-hidden="true">
            {#if i < hadith.narrators.length - 1}
              <span class="isnad__hop-line"></span>
            {/if}
            <span class="isnad__hop-dot"></span>
          </span>
          <div class="isnad__hop-body">
            <div class="isnad__hop-name" dir="rtl">{n.nameAr}</div>
            <div class="isnad__hop-en">{n.name}</div>
            <div class="isnad__hop-meta">
              <span class="isnad__hop-role">{n.role}</span>
              <span class="isnad__hop-grade">{n.grade}</span>
              <span class="isnad__hop-d">d. {n.d} AH</span>
            </div>
          </div>
        </li>
      {/each}
    </ol>
  {:else if viz === 'flow'}
    <svg
      class="isnad__flow"
      viewBox="0 0 100 {hadith.narrators.length * 24}"
      preserveAspectRatio="xMidYMin meet"
    >
      <defs>
        <radialGradient id="flow-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="var(--reader-honorific)" stop-opacity="0.5" />
          <stop offset="100%" stop-color="var(--reader-honorific)" stop-opacity="0" />
        </radialGradient>
      </defs>
      {#each hadith.narrators as n, i (i)}
        {@const cy = 14 + i * 24}
        {#if i < hadith.narrators.length - 1}
          <path
            d="M 50 {cy + 4} Q {i % 2 === 0 ? 70 : 30} {cy + 14}, 50 {cy + 24}"
            fill="none"
            stroke="var(--reader-honorific)"
            stroke-width="0.6"
            stroke-dasharray="0.8 1.2"
            opacity="0.55"
          />
        {/if}
        <circle cx="50" {cy} r="6" fill="url(#flow-glow)" opacity="0.6" />
        <circle cx="50" {cy} r="2.4" fill="var(--reader-honorific)" />
        <text
          x="50"
          y={cy + 11}
          text-anchor="middle"
          font-size="3.4"
          fill="var(--reader-fg)"
          font-family="var(--font-arabic)">{n.nameAr}</text
        >
      {/each}
    </svg>
  {:else}
    <div class="isnad__cards">
      {#each hadith.narrators as n, i (i)}
        <div class="isnad__card" style:--card-i={i}>
          <span class="isnad__card-num">{String(i + 1).padStart(2, '0')}</span>
          <div class="isnad__card-name" dir="rtl">{n.nameAr}</div>
          <div class="isnad__card-en">{n.name}</div>
          <div class="isnad__card-grade">{n.grade}</div>
        </div>
      {/each}
    </div>
  {/if}

  {#if hadith.crossRefs.length}
    <div class="isnad__refs">
      <div class="isnad__refs-label">Parallels</div>
      {#each hadith.crossRefs as r, i (i)}
        <div class="isnad__ref">
          <span class="isnad__ref-ar" dir="rtl">{r.bookAr}</span>
          <span class="isnad__ref-en">{r.book} · {r.chapter}, p. {r.page}</span>
        </div>
      {/each}
    </div>
  {/if}
</aside>

<style>
  .isnad {
    border-left: 1px solid var(--reader-rule);
    padding: 28px 22px;
    overflow-y: auto;
    background: color-mix(in oklch, var(--reader-bg) 96%, var(--color-accent) 4%);
  }
  .isnad__head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-bottom: 12px;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--reader-rule);
  }
  .isnad__eyebrow {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.6;
  }
  .isnad__eyebrow-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    color: var(--reader-honorific);
  }
  .isnad__viz-toggle {
    display: flex;
    gap: 4px;
    padding: 3px;
    border: 1px solid var(--reader-rule);
    border-radius: var(--radius-full);
    margin-bottom: 14px;
  }
  :global(.isnad__viz-btn) {
    flex: 1;
    background: transparent;
    border: none;
    padding: 5px 8px;
    border-radius: var(--radius-full);
    color: inherit;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    cursor: pointer;
    transition: background var(--duration-fast) var(--ease-standard);
  }
  :global(.isnad__viz-btn:hover) {
    background: color-mix(in oklch, var(--reader-honorific) 12%, transparent);
  }
  :global(.isnad__viz-btn.is-active) {
    background: var(--reader-honorific);
    color: var(--reader-bg);
  }

  .isnad__intro {
    margin: 0 0 18px;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    line-height: 1.55;
    opacity: 0.8;
  }

  .isnad__flow {
    width: 100%;
    display: block;
    margin-bottom: 22px;
  }

  .isnad__cards {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 22px;
  }
  .isnad__card {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: baseline;
    gap: 10px;
    padding: 10px 12px;
    border: 1px solid var(--reader-rule);
    border-radius: var(--radius-sm);
    background: color-mix(in oklch, var(--reader-bg) 92%, var(--reader-honorific) 8%);
    transform: translateX(calc(var(--card-i) * 4px));
    transition: transform var(--duration-fast) var(--ease-standard);
  }
  .isnad__card:hover {
    transform: translateX(0);
  }
  .isnad__card-num {
    grid-row: span 3;
    align-self: start;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--reader-honorific);
    letter-spacing: 0.14em;
  }
  .isnad__card-name {
    grid-column: 2 / 4;
    font-family: var(--font-arabic);
    font-size: var(--text-base);
    font-weight: 700;
    color: var(--reader-honorific);
  }
  .isnad__card-en {
    grid-column: 2 / 4;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
  }
  .isnad__card-grade {
    grid-column: 2 / 4;
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--color-success);
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }
  .isnad__intro em {
    font-style: italic;
    color: var(--reader-honorific);
    font-weight: 600;
  }

  .isnad__list {
    list-style: none;
    margin: 0 0 22px;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .isnad__hop {
    display: grid;
    grid-template-columns: 18px 1fr;
    gap: 12px;
  }
  .isnad__hop-mark {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 6px;
  }
  .isnad__hop-dot {
    width: 10px;
    height: 10px;
    border-radius: var(--radius-full);
    background: var(--reader-honorific);
    box-shadow: 0 0 8px color-mix(in oklch, var(--reader-honorific) 50%, transparent);
    z-index: 1;
  }
  .isnad__hop-line {
    position: absolute;
    top: 16px;
    bottom: -16px;
    left: 50%;
    width: 1px;
    background: linear-gradient(to bottom, var(--reader-honorific), transparent);
    transform: translateX(-50%);
  }

  .isnad__hop-body {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .isnad__hop-name {
    font-family: var(--font-arabic);
    font-size: var(--text-base);
    font-weight: 700;
    color: var(--reader-honorific);
    line-height: 1.3;
  }
  .isnad__hop-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
  }
  .isnad__hop-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 10px;
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.6;
  }
  .isnad__hop-grade {
    color: var(--color-success);
  }

  .isnad__refs {
    border-top: 1px solid var(--reader-rule);
    padding-top: 14px;
  }
  .isnad__refs-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 10px;
  }
  .isnad__ref {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 8px 0;
    border-bottom: 1px dashed var(--reader-rule);
  }
  .isnad__ref:last-child {
    border-bottom: none;
  }
  .isnad__ref-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    color: var(--reader-honorific);
  }
  .isnad__ref-en {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.65;
  }
</style>
