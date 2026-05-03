<script lang="ts">
  import Badge from '../primitives/Badge.svelte';
  import { healthBandToStatus, healthBandLabel, type HealthBand } from '../variants.js';

  interface Props {
    band: HealthBand;
    score?: number | null | undefined;
    class?: string | undefined;
  }

  let { band, score = null, class: extra = '' }: Props = $props();

  const status = $derived(healthBandToStatus[band]);
  const label = $derived(healthBandLabel[band]);
</script>

<Badge {status} size="sm" class={extra}>
  {#if score !== null && score !== undefined}{Math.round(score)} ·{/if}
  {label}
</Badge>
