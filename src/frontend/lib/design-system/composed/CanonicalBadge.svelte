<!--
  src/frontend/lib/design-system/composed/CanonicalBadge.svelte

  Renders a book's canonical tier (primary / secondary / commentary / reference).
  Composes Badge — color comes from variants.ts, never inline.
-->
<script lang="ts">
  import Badge from '../primitives/Badge.svelte';
  import { canonicalTierToStatus, canonicalTierLabel, type CanonicalTier } from '../variants.js';

  interface Props {
    tier: CanonicalTier;
    variant?: 'soft' | 'outline';
    size?: 'sm' | 'md';
    class?: string | undefined;
  }

  let { tier, variant = 'soft', size = 'sm', class: extra = '' }: Props = $props();

  const status = $derived(canonicalTierToStatus[tier]);
  const label = $derived(canonicalTierLabel[tier]);
</script>

<Badge {status} {variant} {size} class={extra}>{label}</Badge>
