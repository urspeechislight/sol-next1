<!--
  Manuscript-style geometric corner cartouche, used at the four corners
  of the hero. The same path renders at each corner; rotation positions
  it so the L-shape opens toward the centre.
-->
<script lang="ts">
  type Pos = 'tl' | 'tr' | 'bl' | 'br';
  interface Props {
    pos: Pos;
  }

  let { pos }: Props = $props();
  const rotation: Record<Pos, number> = { tl: 0, tr: 90, br: 180, bl: 270 };
</script>

<svg
  class="corner corner--{pos}"
  width="56"
  height="56"
  viewBox="0 0 56 56"
  aria-hidden="true"
  style:--corner-rotation="{rotation[pos]}deg"
>
  <g
    fill="none"
    stroke="var(--color-accent)"
    stroke-width="0.7"
    stroke-linecap="round"
    stroke-linejoin="round"
    opacity="0.5"
  >
    <path d="M2 26V2h24" />
    <path d="M2 16V8h8" opacity="0.8" />
    <circle cx="6" cy="6" r="1.3" fill="var(--color-accent)" stroke="none" />
    <path d="M14 2c4 4 6 8 6 14M2 22c4 0 8 -2 14 -6" opacity="0.4" />
  </g>
</svg>

<style>
  .corner {
    position: absolute;
    pointer-events: none;
    transform: rotate(var(--corner-rotation, 0deg));
  }
  .corner--tl {
    top: 16px;
    left: 16px;
  }
  .corner--tr {
    top: 16px;
    right: 16px;
  }
  .corner--bl {
    bottom: 16px;
    left: 16px;
  }
  .corner--br {
    bottom: 16px;
    right: 16px;
  }
</style>
