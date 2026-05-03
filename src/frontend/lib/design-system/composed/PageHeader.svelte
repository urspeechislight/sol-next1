<script lang="ts">
  import type { Snippet } from 'svelte';
  import Stack from '../primitives/Stack.svelte';
  import Text from '../primitives/Text.svelte';

  type Props = {
    title: string;
    subtitle?: string | undefined;
    actions?: Snippet | undefined;
    class?: string | undefined;
  };

  let { title, subtitle, actions, class: extra = '' }: Props = $props();
</script>

<header class="border-b border-border-1 pb-6 mb-8 {extra}">
  <Stack direction="row" align="end" justify="between" gap={4} wrap>
    <Stack gap={1}>
      <Text as="h1" size="3xl" weight="semibold" family="display" class="tracking-tight">
        {title}
      </Text>
      {#if subtitle}
        <Text tone="secondary">{subtitle}</Text>
      {/if}
    </Stack>
    {#if actions}
      <div>{@render actions()}</div>
    {/if}
  </Stack>
</header>
