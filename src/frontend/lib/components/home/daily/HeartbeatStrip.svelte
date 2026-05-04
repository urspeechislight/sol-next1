<!--
  Heartbeat strip — 60 ticks across the bottom of the instrument with
  a rolling gold comet that ticks once per second. Anchors the trio
  above as a single instrument with a live clock.
-->
<script lang="ts">
  interface Props {
    tick: number;
  }
  let { tick }: Props = $props();
  const N = 60;
  const ticks = Array.from({ length: N }, (_, i) => i);
  const cometIdx = $derived(tick % N);
</script>

<div class="hb" aria-hidden="true">
  <div class="hb__rail">
    {#each ticks as i (i)}
      {@const distance = (cometIdx - i + N) % N}
      {@const heat = distance < 6 ? (6 - distance) / 6 : 0}
      <span class="hb__tick" class:major={i % 6 === 0} style:--heat={heat.toFixed(2)}></span>
    {/each}
  </div>
  <span class="hb__label">{String(tick).padStart(4, '0')} t</span>
</div>

<style>
  .hb {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0 4px;
    border-top: 1px solid var(--color-border-1);
    margin-top: 8px;
  }
  .hb__rail {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(60, 1fr);
    align-items: center;
    height: 14px;
    gap: 1px;
  }
  .hb__tick {
    height: 6px;
    background: var(--color-border-1);
    border-radius: 1px;
    box-shadow: 0 0 calc(8px * var(--heat, 0)) var(--color-accent);
    transition:
      background 380ms ease,
      box-shadow 380ms ease;
  }
  .hb__tick.major {
    height: 10px;
    background: var(--color-border-2);
  }
  .hb__tick {
    background-color: color-mix(
      in oklch,
      var(--color-accent) calc(var(--heat, 0) * 100%),
      var(--color-border-1)
    );
  }
  .hb__label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-fg-3);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    flex-shrink: 0;
  }
</style>
