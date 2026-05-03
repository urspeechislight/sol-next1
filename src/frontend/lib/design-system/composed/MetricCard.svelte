<script lang="ts">
  import Card from '../primitives/Card.svelte';
  import Stack from '../primitives/Stack.svelte';
  import Text from '../primitives/Text.svelte';
  import { trendToStatus, trendGlyph, type TrendDirection } from '../variants.js';

  type Props = {
    label: string;
    value: string | number;
    trend?: TrendDirection | undefined;
    delta?: string | undefined;
    class?: string | undefined;
  };

  let { label, value, trend, delta, class: extra = '' }: Props = $props();

  const trendStatus = $derived(trend ? trendToStatus[trend] : null);
</script>

<Card class={extra}>
  <Stack gap={2}>
    <Text size="sm" tone="secondary">{label}</Text>
    <Text size="3xl" weight="semibold" family="display" class="tracking-tight">
      {value}
    </Text>
    {#if trend && delta}
      <Stack direction="row" gap={1} align="center">
        <Text size="sm" tone={trendStatus ?? 'secondary'} weight="medium">
          {trendGlyph[trend]} {delta}
        </Text>
      </Stack>
    {/if}
  </Stack>
</Card>
