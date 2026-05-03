<!--
  src/frontend/lib/design-system/composed/SectionHead.svelte

  Section header for grouped content (e.g. "Foundational Works", "Tafasir").
  Mono eyebrow + display title + optional action snippet on the right.
-->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import Stack from '../primitives/Stack.svelte';
  import Text from '../primitives/Text.svelte';

  interface Props {
    eyebrow?: string | undefined;
    title: string;
    actions?: Snippet | undefined;
    class?: string | undefined;
  }

  let { eyebrow, title, actions, class: extra = '' }: Props = $props();
</script>

<header class="border-border-1 mb-4 border-b pb-3 {extra}">
  <Stack direction="row" align="end" justify="between" gap={4} wrap>
    <Stack gap={1}>
      {#if eyebrow}
        <Text size="xs" tone="tertiary" family="mono" class="uppercase tracking-wide">
          {eyebrow}
        </Text>
      {/if}
      <Text as="h2" size="2xl" weight="semibold" family="display" class="tracking-tight">
        {title}
      </Text>
    </Stack>
    {#if actions}
      <div>{@render actions()}</div>
    {/if}
  </Stack>
</header>
