<!--
  src/frontend/lib/design-system/composed/SectBadge.svelte

  Renders a sect (Imami / Sunni / Zaidi / ...) with the canonical color mapping.
  Composes Badge primitive — never picks a color directly.
-->
<script lang="ts">
  import Badge from '../primitives/Badge.svelte';
  import { sectToStatus, sectLabel, type Sect } from '../variants.js';

  interface Props {
    sect: Sect;
    variant?: 'soft' | 'outline';
    size?: 'sm' | 'md';
    class?: string | undefined;
  }

  let { sect, variant = 'outline', size = 'sm', class: extra = '' }: Props = $props();

  const status = $derived(sectToStatus[sect]);
  const label = $derived(sectLabel[sect]);
</script>

<Badge {status} {variant} {size} class={extra}>{label}</Badge>
