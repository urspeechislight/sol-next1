<!--
  Colophon — closes the page in the manuscript convention: a slowly
  rotating star ornament, a verse, and the build metadata.
-->
<script lang="ts">
  // Static — no reactive state needed.
</script>

<footer class="colophon">
  <div class="colophon__ornament" aria-hidden="true">
    <svg viewBox="-12 -12 24 24" width="64" height="64">
      <g
        fill="none"
        stroke="var(--color-accent)"
        stroke-width="0.6"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="0" cy="0" r="10" opacity="0.5" />
        <circle cx="0" cy="0" r="6" opacity="0.7" />
        <circle cx="0" cy="0" r="1.4" fill="var(--color-accent)" stroke="none" />
        {#each [0, 45, 90, 135] as a (a)}
          {@const r = (a * Math.PI) / 180}
          <line
            x1={(Math.cos(r) * 6).toFixed(2)}
            y1={(Math.sin(r) * 6).toFixed(2)}
            x2={(Math.cos(r) * 10).toFixed(2)}
            y2={(Math.sin(r) * 10).toFixed(2)}
            opacity="0.6"
          />
          <line
            x1={(Math.cos(r + Math.PI) * 6).toFixed(2)}
            y1={(Math.sin(r + Math.PI) * 6).toFixed(2)}
            x2={(Math.cos(r + Math.PI) * 10).toFixed(2)}
            y2={(Math.sin(r + Math.PI) * 10).toFixed(2)}
            opacity="0.6"
          />
        {/each}
      </g>
    </svg>
  </div>

  <p class="colophon__verse" dir="rtl">وَقُل رَّبِّ زِدْنِي عِلْمًا</p>
  <p class="colophon__transliteration">
    <em>Wa-qul rabbi zidnī ʿilmā</em> · And say: My Lord, increase me in knowledge
  </p>

  <div class="colophon__meta">
    <span>Sol</span>
    <span class="colophon__sep">·</span>
    <span>A reading instrument for the Islamic textual tradition</span>
    <span class="colophon__sep">·</span>
    <span>Vol. I</span>
  </div>
</footer>

<style>
  .colophon {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 88px 32px 64px;
    max-width: 720px;
    margin: 64px auto 0;
    color: var(--color-fg-2);
  }
  .colophon__ornament {
    display: inline-block;
    margin-bottom: 22px;
    animation: orn-rotate 80s linear infinite;
  }
  @keyframes orn-rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .colophon__verse {
    margin: 0 0 12px;
    font-family: var(--font-arabic);
    font-size: var(--text-3xl);
    font-weight: 700;
    color: var(--color-fg-1);
    line-height: 1.4;
  }
  .colophon__transliteration {
    margin: 0 0 32px;
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-base);
    color: var(--color-fg-2);
  }
  .colophon__meta {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    text-transform: uppercase;
    letter-spacing: 0.18em;
  }
  .colophon__sep {
    color: var(--color-accent);
    opacity: 0.45;
  }
</style>
