<!--
  Iconographic glyph for each of the seven knowledge domains, drawn at
  48x48 inside each cabinet drawer. The SVG paths are intentionally
  spare so they read at small sizes and tonally as ink-on-vellum.

  Glyph vocabulary (echoed from the design prototype):
    hadith     chain links   transmission
    quran      open codex    the recited book
    fiqh       balance scale jurisprudence
    theology   concentric arcs  kalam, doctrine
    biography  arched portal figure   sira / tarajim
    sciences   astrolabe / starburst  sciences
    devotional crescent + bead  ethics, du`a, devotional
-->
<script lang="ts">
  interface Props {
    id: string;
    size?: number | undefined;
    class?: string | undefined;
  }

  let { id, size = 48, class: extra = '' }: Props = $props();
</script>

<svg
  viewBox="-12 -12 24 24"
  width={size}
  height={size}
  fill="none"
  stroke="currentColor"
  stroke-width="0.7"
  stroke-linecap="round"
  stroke-linejoin="round"
  class={extra}
  aria-hidden="true"
>
  {#if id === 'hadith'}
    <rect x="-5" y="-1.6" width="4.2" height="3.2" rx="1.6" />
    <rect x="0.8" y="-1.6" width="4.2" height="3.2" rx="1.6" />
    <line x1="-0.8" y1="0" x2="0.8" y2="0" />
  {:else if id === 'quran'}
    <path d="M-5 -3.5C-3 -4.2 -1 -4.2 0 -3v7c-1.6-0.6-3-0.6-5 0z" />
    <path d="M5 -3.5C3 -4.2 1 -4.2 0 -3v7c1.6-0.6 3-0.6 5 0z" />
    <line x1="0" y1="-3" x2="0" y2="4" />
  {:else if id === 'fiqh'}
    <line x1="0" y1="-4.5" x2="0" y2="4.5" />
    <line x1="-3.5" y1="-3" x2="3.5" y2="-3" />
    <path d="M-3.5 -3l-1.6 3.2c0 1.1 0.8 1.7 1.6 1.7s1.6-0.6 1.6-1.7z" />
    <path d="M3.5 -3l-1.6 3.2c0 1.1 0.8 1.7 1.6 1.7s1.6-0.6 1.6-1.7z" />
    <line x1="-2" y1="4.5" x2="2" y2="4.5" />
  {:else if id === 'theology'}
    <circle cx="0" cy="0" r="1.1" />
    <path d="M-3.2 0a3.2 3.2 0 0 1 6.4 0" />
    <path d="M-4.8 0a4.8 4.8 0 0 1 9.6 0" />
  {:else if id === 'biography'}
    <path d="M-3.8 4.5V-1a3.8 3.8 0 0 1 7.6 0V4.5" />
    <circle cx="0" cy="-1" r="1.1" />
    <path d="M-1.6 2.8c0-0.9 0.7-1.6 1.6-1.6s1.6 0.7 1.6 1.6V4.5" />
  {:else if id === 'sciences'}
    <circle cx="0" cy="0" r="3.5" />
    <line x1="0" y1="-3.5" x2="0" y2="3.5" />
    <line x1="-3.5" y1="0" x2="3.5" y2="0" />
    <line x1="-2.5" y1="-2.5" x2="2.5" y2="2.5" opacity="0.7" />
    <line x1="-2.5" y1="2.5" x2="2.5" y2="-2.5" opacity="0.7" />
  {:else if id === 'devotional'}
    <path d="M2 -4a4 4 0 1 0 0 8 3 3 0 0 1 0 -8z" />
    <circle cx="-1.5" cy="0" r="0.4" fill="currentColor" />
  {:else}
    <circle cx="0" cy="0" r="3" />
  {/if}
</svg>
