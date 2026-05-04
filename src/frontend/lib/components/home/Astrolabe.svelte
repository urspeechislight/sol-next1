<!--
  Astrolabe — the rotating "domains of knowledge" centerpiece for the
  hero. Concentric rings: outer dial with 72 tick marks (major every
  6th), mid orbital path, inner cardinal cross + medallion with the
  Arabic letter ع. Seven orbital nodes — one per domain — sit on the
  mid ring at evenly-spaced angles starting at -90deg (top).

  Motion: the outer dial rotates clockwise on a 60s loop; the mid ring
  counter-rotates on 90s. The orbital nodes themselves are anchored to
  the static svg so their positions don't drift; hover scales the inner
  group only (the outer translate stays put — this avoids the "spasm"
  where competing transforms reset position).

  Click a node to enter that domain's first category in /library.
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { DOMAINS } from '$lib/fixtures';

  let hover = $state<number | null>(null);

  // Layout: 7 nodes evenly placed on a circle. Start at -90deg (top), go CW.
  const N = DOMAINS.length;
  const RADIUS = 38; // % of svg viewBox half-width (which is 100)
  const ORBIT = RADIUS * 1.6; // 60.8

  const nodes = $derived.by(() => {
    return DOMAINS.map((d, i) => {
      const a = -Math.PI / 2 + (i / N) * Math.PI * 2;
      return {
        id: d.id,
        labelEn: d.label,
        labelAr: d.labelAr,
        slug: d.categories[0]?.slug,
        cx: Math.cos(a) * ORBIT,
        cy: Math.sin(a) * ORBIT,
        ax: Math.cos(a) * 22,
        ay: Math.sin(a) * 22,
      };
    });
  });

  const ticks = Array.from({ length: 72 }, (_, i) => {
    const a = (i / 72) * Math.PI * 2;
    const isMajor = i % 6 === 0;
    const r1 = 86;
    const r2 = isMajor ? 80 : 83;
    return {
      x1: Math.cos(a) * r1,
      y1: Math.sin(a) * r1,
      x2: Math.cos(a) * r2,
      y2: Math.sin(a) * r2,
      isMajor,
    };
  });

  const activeDomain = $derived(hover != null ? DOMAINS[hover] : null);

  function go(slug: string | undefined) {
    if (!slug) return;
    void goto(`/library/${slug}`);
  }
</script>

<div class="astro">
  <svg viewBox="-100 -100 200 200" class="astro__svg" aria-label="Domains of knowledge">
    <defs>
      <radialGradient id="astro-glow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="var(--color-accent)" stop-opacity="0.25" />
        <stop offset="60%" stop-color="var(--color-accent)" stop-opacity="0.08" />
        <stop offset="100%" stop-color="var(--color-accent)" stop-opacity="0" />
      </radialGradient>
    </defs>

    <circle cx="0" cy="0" r="90" fill="url(#astro-glow)" />

    <!-- outer rotating dial -->
    <g class="astro__ring astro__ring--outer">
      <circle
        cx="0"
        cy="0"
        r="86"
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="0.6"
        opacity="0.7"
      />
      {#each ticks as t, i (i)}
        <line
          x1={t.x1.toFixed(2)}
          y1={t.y1.toFixed(2)}
          x2={t.x2.toFixed(2)}
          y2={t.y2.toFixed(2)}
          stroke="var(--color-accent)"
          stroke-width={t.isMajor ? 0.6 : 0.3}
          opacity={t.isMajor ? 0.7 : 0.35}
        />
      {/each}
    </g>

    <!-- mid orbital ring -->
    <g class="astro__ring astro__ring--mid">
      <circle
        cx="0"
        cy="0"
        r={ORBIT.toFixed(2)}
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="0.4"
        stroke-dasharray="0.8 1.2"
        opacity="0.5"
      />
    </g>

    <!-- inner cardinal cross + medallion -->
    <g class="astro__ring astro__ring--inner">
      <circle
        cx="0"
        cy="0"
        r="22"
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="0.5"
        opacity="0.6"
      />
      <circle
        cx="0"
        cy="0"
        r="14"
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="0.4"
        opacity="0.4"
      />
      <line
        x1="-22"
        y1="0"
        x2="22"
        y2="0"
        stroke="var(--color-accent)"
        stroke-width="0.3"
        opacity="0.4"
      />
      <line
        x1="0"
        y1="-22"
        x2="0"
        y2="22"
        stroke="var(--color-accent)"
        stroke-width="0.3"
        opacity="0.4"
      />
      <circle
        cx="0"
        cy="0"
        r="5"
        fill="var(--color-bg-0)"
        stroke="var(--color-accent)"
        stroke-width="0.6"
      />
      <text
        x="0"
        y="0"
        text-anchor="middle"
        dominant-baseline="central"
        font-family="var(--font-arabic)"
        font-size="6"
        font-weight="700"
        fill="var(--color-accent)">ع</text
      >
    </g>

    <!-- sigil rays from medallion to each node -->
    <g class="astro__rays">
      {#each nodes as n, i (n.id)}
        <line
          x1={n.ax.toFixed(2)}
          y1={n.ay.toFixed(2)}
          x2={n.cx.toFixed(2)}
          y2={n.cy.toFixed(2)}
          stroke="var(--color-accent)"
          stroke-width="0.3"
          opacity={hover === i ? 0.9 : 0.25}
          stroke-dasharray="0.4 0.6"
        />
      {/each}
    </g>

    <!-- orbital nodes — outer g translates, inner g scales on hover -->
    {#each nodes as n, i (n.id)}
      {@const isHover = hover === i}
      <g
        class="astro__node"
        transform="translate({n.cx.toFixed(2)} {n.cy.toFixed(2)})"
        role="button"
        tabindex="0"
        aria-label={n.labelEn}
        onmouseenter={() => (hover = i)}
        onmouseleave={() => (hover = null)}
        onfocus={() => (hover = i)}
        onblur={() => (hover = null)}
        onclick={() => go(n.slug)}
        onkeydown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            go(n.slug);
          }
        }}
      >
        <g class="astro__node-inner">
          <circle
            r="9"
            fill="none"
            stroke="var(--color-accent)"
            stroke-width="0.5"
            opacity={isHover ? 0.9 : 0.5}
          />
          <circle
            r="6"
            fill={isHover ? 'var(--color-accent)' : 'var(--color-bg-0)'}
            stroke="var(--color-accent)"
            stroke-width="0.8"
          />
          <g
            transform="scale(0.55)"
            stroke={isHover ? 'var(--color-bg-0)' : 'var(--color-accent)'}
            fill="none"
            stroke-width="1.2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            {#if n.id === 'hadith'}
              <rect x="-5" y="-1.6" width="4.2" height="3.2" rx="1.6" />
              <rect x="0.8" y="-1.6" width="4.2" height="3.2" rx="1.6" />
              <line x1="-0.8" y1="0" x2="0.8" y2="0" />
            {:else if n.id === 'quran'}
              <path d="M-5 -3.5C-3 -4.2 -1 -4.2 0 -3v7c-1.6-0.6-3-0.6-5 0z" />
              <path d="M5 -3.5C3 -4.2 1 -4.2 0 -3v7c1.6-0.6 3-0.6 5 0z" />
              <line x1="0" y1="-3" x2="0" y2="4" />
            {:else if n.id === 'fiqh'}
              <line x1="0" y1="-4.5" x2="0" y2="4.5" />
              <line x1="-3.5" y1="-3" x2="3.5" y2="-3" />
              <path d="M-3.5 -3l-1.6 3.2c0 1.1 0.8 1.7 1.6 1.7s1.6-0.6 1.6-1.7z" />
              <path d="M3.5 -3l-1.6 3.2c0 1.1 0.8 1.7 1.6 1.7s1.6-0.6 1.6-1.7z" />
              <line x1="-2" y1="4.5" x2="2" y2="4.5" />
            {:else if n.id === 'theology'}
              <circle cx="0" cy="0" r="1.1" />
              <path d="M-3.2 0a3.2 3.2 0 0 1 6.4 0" />
              <path d="M-4.8 0a4.8 4.8 0 0 1 9.6 0" />
            {:else if n.id === 'biography'}
              <path d="M-3.8 4.5V-1a3.8 3.8 0 0 1 7.6 0V4.5" />
              <circle cx="0" cy="-1" r="1.1" />
              <path d="M-1.6 2.8c0-0.9 0.7-1.6 1.6-1.6s1.6 0.7 1.6 1.6V4.5" />
            {:else if n.id === 'sciences'}
              <circle cx="0" cy="0" r="3.5" />
              <line x1="0" y1="-3.5" x2="0" y2="3.5" />
              <line x1="-3.5" y1="0" x2="3.5" y2="0" />
              <line x1="-2.5" y1="-2.5" x2="2.5" y2="2.5" opacity="0.7" />
              <line x1="-2.5" y1="2.5" x2="2.5" y2="-2.5" opacity="0.7" />
            {:else if n.id === 'devotional'}
              <path d="M2 -4a4 4 0 1 0 0 8 3 3 0 0 1 0 -8z" />
              <circle cx="-1.5" cy="0" r="0.4" fill="currentColor" />
            {/if}
          </g>
        </g>
      </g>
    {/each}
  </svg>

  <div class="astro__legend" aria-live="polite">
    {#if activeDomain && hover != null}
      <span class="astro__legend-num">§ {String(hover + 1).padStart(2, '0')}</span>
      <div class="astro__legend-text">
        <span class="astro__legend-en">{activeDomain.label}</span>
        <span class="astro__legend-ar" dir="rtl">{activeDomain.labelAr}</span>
      </div>
      <span class="astro__legend-cta">Open →</span>
    {:else}
      <span class="astro__legend-hint">Hover a node to inspect · click to enter</span>
    {/if}
  </div>
</div>

<style>
  .astro {
    position: relative;
    width: 100%;
    aspect-ratio: 1 / 1;
    max-width: 460px;
    margin-inline: auto;
  }
  .astro__svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  .astro__ring--outer {
    transform-origin: center;
    animation: astro-spin 60s linear infinite;
  }
  .astro__ring--mid {
    transform-origin: center;
    animation: astro-spin-rev 90s linear infinite;
  }
  @keyframes astro-spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes astro-spin-rev {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(-360deg);
    }
  }

  .astro__node {
    cursor: pointer;
    outline: none;
  }
  .astro__node-inner {
    transform-box: fill-box;
    transform-origin: center;
    transition: transform var(--duration-normal) var(--ease-standard);
  }
  .astro__node:hover .astro__node-inner,
  .astro__node:focus-visible .astro__node-inner {
    transform: scale(1.18);
  }

  .astro__legend {
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translate(-50%, 100%);
    display: flex;
    align-items: baseline;
    gap: 12px;
    padding: 8px 16px;
    background: var(--color-bg-1);
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-sm);
    white-space: nowrap;
    box-shadow: var(--shadow-md);
    min-height: 36px;
  }
  .astro__legend-num {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-accent);
    letter-spacing: var(--tracking-wide);
  }
  .astro__legend-text {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }
  .astro__legend-en {
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-fg-1);
  }
  .astro__legend-ar {
    font-family: var(--font-arabic);
    font-size: var(--text-sm);
    color: var(--color-accent);
  }
  .astro__legend-cta {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-fg-3);
    text-transform: uppercase;
    letter-spacing: var(--tracking-wide);
  }
  .astro__legend-hint {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-fg-3);
    text-transform: uppercase;
    letter-spacing: var(--tracking-wide);
  }
</style>
