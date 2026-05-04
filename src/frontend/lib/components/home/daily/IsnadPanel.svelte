<!--
  Isnad panel — animated SVG narrator chain that draws itself node-by-
  node, then reveals the matn beneath via clip-path. Restarts every
  ~10s so the panel reads as a working instrument.
-->
<script lang="ts">
  import type { HadithOfDay } from '$lib/fixtures';

  interface Props {
    hadith: HadithOfDay;
  }
  let { hadith }: Props = $props();

  // Synthetic 3-hop chain inferred from the data: source → companion → Prophet.
  const chain = $derived([
    { id: 'src', en: hadith.source.book, ar: hadith.source.bookAr, kind: 'source' },
    { id: 'narr', en: 'Abū al-Dardāʾ', ar: 'أبي الدرداء', kind: 'companion' },
    { id: 'prophet', en: 'The Prophet', ar: 'النبي ﷺ', kind: 'prophet' },
  ]);

  const CYCLE = 10000;
  const HOPS = 4; // 3 nodes + 1 beat for the matn reveal
  const PER_HOP = CYCLE / HOPS;

  let t0 = $state(0);
  let now = $state(0);
  $effect(() => {
    t0 = performance.now();
    let raf = 0;
    const frame = () => {
      now = performance.now();
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  });
  const elapsed = $derived((now - t0) % CYCLE || 0);
  const phase = $derived(elapsed / PER_HOP); // 0..HOPS

  // Layout: nodes at x=20, 50, 80 (svg coords). Tuple type so positions[i]
  // is statically known to be a number.
  const positions = [20, 50, 80] as const;

  function nodeProgress(i: number): number {
    return Math.max(0, Math.min(1, phase - i));
  }
</script>

<article class="panel">
  <div class="panel__eyebrow">
    <span class="panel__eyebrow-num">II</span>
    <span class="panel__eyebrow-label">Isnād</span>
    <span class="panel__eyebrow-live" aria-hidden="true"></span>
    <span class="panel__eyebrow-sub">{hadith.gradeLabel}</span>
  </div>

  <h3 class="panel__title">
    <em>Chain</em> of Transmission
  </h3>

  <div class="isnad__viz">
    <svg viewBox="0 0 100 38" class="isnad__svg" aria-hidden="true">
      <defs>
        <radialGradient id="isnad-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="var(--color-accent)" stop-opacity="0.5" />
          <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- edges drawn one by one -->
      {#each [0, 1] as i (i)}
        {@const x1 = (positions[i as 0 | 1] as number) + 4}
        {@const x2 = (positions[(i + 1) as 1 | 2] as number) - 4}
        {@const length = x2 - x1}
        {@const t = nodeProgress(i + 1)}
        <line
          {x1}
          y1="20"
          x2={(x1 + length * t).toFixed(2)}
          y2="20"
          stroke="var(--color-accent)"
          stroke-width="0.4"
          stroke-dasharray="0.6 0.4"
          opacity="0.85"
        />
        <!-- عَنْ marker -->
        <text
          x={((x1 + x2) / 2).toFixed(2)}
          y="14"
          text-anchor="middle"
          font-family="var(--font-arabic)"
          font-size="2.6"
          fill="var(--color-fg-3)"
          opacity={t > 0.3 ? '0.8' : '0'}>عَنْ</text
        >
      {/each}

      <!-- nodes -->
      {#each chain as c, i (c.id)}
        {@const t = nodeProgress(i)}
        {@const reached = t > 0.4}
        {@const isProphet = c.kind === 'prophet'}
        {@const cx = positions[i as 0 | 1 | 2]}
        <g transform="translate({cx} 20)">
          {#if reached}
            <circle r={isProphet ? 6 : 5} fill="url(#isnad-glow)" opacity={isProphet ? 0.9 : 0.6} />
          {/if}
          <circle
            r={isProphet ? 3.4 : 2.6}
            fill={reached ? 'var(--color-accent)' : 'var(--color-bg-2)'}
            stroke="var(--color-accent)"
            stroke-width="0.4"
          />
          <text
            x="0"
            y={isProphet ? 11 : 10}
            text-anchor="middle"
            font-family="var(--font-arabic)"
            font-size="2.8"
            fill={reached ? 'var(--color-fg-1)' : 'var(--color-fg-3)'}>{c.ar}</text
          >
        </g>
      {/each}
    </svg>
  </div>

  <div class="matn">
    <div
      class="matn__inner"
      dir="rtl"
      style:--matn-clip="{Math.max(0, Math.min(1, phase - 3)) * 100}%"
    >
      {hadith.matnAr}
    </div>
  </div>

  <p class="isnad__en">{hadith.matnEn}</p>

  <div class="isnad__foot">
    <span class="isnad__grade">{hadith.gradeLabel}</span>
    <span class="isnad__sep">·</span>
    <span class="isnad__parallels-label">Parallels</span>
    {#each hadith.parallels as p, i (i)}
      <span class="isnad__parallel">
        <span class="isnad__parallel-en">{p.book}</span>
      </span>
    {/each}
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
    color: var(--color-success);
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

  .isnad__viz {
    background:
      radial-gradient(ellipse at 50% 50%, var(--color-bg-night-1) 0%, transparent 80%),
      var(--color-bg-1);
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-md);
    padding: 12px;
  }
  .isnad__svg {
    width: 100%;
    height: 110px;
    display: block;
  }

  .matn {
    border-left: 2px solid var(--color-accent);
    padding-left: 14px;
  }
  .matn__inner {
    font-family: var(--font-arabic);
    font-size: var(--text-base);
    line-height: 1.9;
    color: var(--color-fg-1);
    clip-path: inset(0 calc(100% - var(--matn-clip, 0%)) 0 0);
    transition: clip-path 100ms linear;
  }

  .isnad__en {
    margin: 0;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    line-height: 1.6;
    color: var(--color-fg-2);
  }

  .isnad__foot {
    display: flex;
    align-items: baseline;
    gap: 8px;
    flex-wrap: wrap;
    border-top: 1px solid var(--color-border-1);
    padding-top: 10px;
    font-family: var(--font-mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.16em;
  }
  .isnad__grade {
    color: var(--color-success);
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    text-transform: none;
    letter-spacing: 0;
  }
  .isnad__sep {
    color: var(--color-accent);
    opacity: 0.5;
  }
  .isnad__parallels-label {
    color: var(--color-fg-3);
  }
  .isnad__parallel-en {
    color: var(--color-fg-2);
    text-transform: none;
    letter-spacing: 0;
  }
</style>
