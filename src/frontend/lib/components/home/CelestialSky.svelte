<!--
  Full-page celestial backdrop. Lives behind every section as a fixed-
  position layer so the home page reads as one continuous sky from hero
  to colophon.

  Composition:
    - dawn halo at top-left (warm gold radial)
    - dusk halo at bottom-right (deep indigo radial)
    - scholarly hairline grid
    - deterministic star field (~140 stars, fixed seed so SSR / hydrate
      don't mismatch and so the layout stays stable across reloads)
-->
<script lang="ts">
  // Park-Miller / Lehmer LCG — gives us a deterministic pseudo-random
  // sequence so the star field renders identically on the server and
  // client (no hydration mismatch) and across reloads.
  function* prng(seed: number) {
    let s = seed % 2147483647;
    if (s <= 0) s += 2147483646;
    while (true) {
      s = (s * 16807) % 2147483647;
      yield s / 2147483647;
    }
  }

  interface Star {
    x: number;
    y: number;
    r: number;
    a: number;
    d: number;
  }
  function buildStars(count: number, seed: number): Star[] {
    const r = prng(seed);
    const pop: Star[] = [];
    for (let i = 0; i < count; i++) {
      pop.push({
        x: r.next().value as number,
        y: r.next().value as number,
        r: 0.4 + (r.next().value as number) * 1.4,
        a: 0.25 + (r.next().value as number) * 0.55,
        d: (r.next().value as number) * 6,
      });
    }
    return pop;
  }

  const stars = buildStars(140, 11);
</script>

<div class="sky" aria-hidden="true">
  <div class="sky__halo sky__halo--dawn"></div>
  <div class="sky__halo sky__halo--dusk"></div>
  <div class="sky__grid"></div>
  <svg class="sky__stars" viewBox="0 0 100 100" preserveAspectRatio="none">
    {#each stars as s, i (i)}
      <circle
        cx={(s.x * 100).toFixed(3)}
        cy={(s.y * 100).toFixed(3)}
        r={s.r.toFixed(3)}
        opacity={s.a.toFixed(3)}
        style:--twinkle-delay="{s.d.toFixed(2)}s"
        class="sky__star"
      />
    {/each}
  </svg>
</div>

<style>
  .sky {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    background:
      radial-gradient(ellipse at 50% 0%, var(--color-bg-night-1) 0%, transparent 60%),
      radial-gradient(ellipse at 100% 100%, var(--color-bg-night-2) 0%, transparent 70%),
      var(--color-bg-0);
  }
  .sky__halo {
    position: absolute;
    width: 60vmax;
    height: 60vmax;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.45;
  }
  .sky__halo--dawn {
    top: -20vmax;
    left: -10vmax;
    background: radial-gradient(circle, var(--color-sky-halo-dawn), transparent 70%);
  }
  .sky__halo--dusk {
    bottom: -20vmax;
    right: -10vmax;
    background: radial-gradient(circle, var(--color-sky-halo-dusk), transparent 70%);
  }
  .sky__grid {
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(to right, var(--color-sky-grid) 1px, transparent 1px),
      linear-gradient(to bottom, var(--color-sky-grid) 1px, transparent 1px);
    background-size: 96px 96px;
    mask-image: radial-gradient(ellipse at 50% 30%, black 30%, transparent 80%);
  }
  .sky__stars {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }
  .sky__star {
    fill: var(--color-sky-star);
    animation: twinkle 6s ease-in-out infinite;
    animation-delay: var(--twinkle-delay, 0s);
  }
  @keyframes twinkle {
    0%,
    100% {
      opacity: var(--starfield-opacity, 0.6);
    }
    50% {
      opacity: 0.15;
    }
  }
</style>
