<!--
  src/frontend/lib/design-system/composed/Breadcrumb.svelte

  Renders a breadcrumb trail from a list of {label, href} items. The last
  item is rendered as plain text (current page); earlier items are anchors.
-->
<script lang="ts">
  import Stack from '../primitives/Stack.svelte';
  import Text from '../primitives/Text.svelte';

  interface Crumb {
    label: string;
    href?: string | undefined;
  }

  interface Props {
    items: Crumb[];
    class?: string | undefined;
  }

  let { items, class: extra = '' }: Props = $props();
</script>

<nav aria-label="Breadcrumb" class={extra}>
  <Stack direction="row" gap={2} align="center" wrap>
    {#each items as crumb, i (crumb.label)}
      {#if i > 0}
        <Text size="xs" tone="tertiary" family="mono">/</Text>
      {/if}
      {#if crumb.href && i < items.length - 1}
        <a href={crumb.href} class="text-fg-2 hover:text-fg-1 font-mono text-sm no-underline">
          {crumb.label}
        </a>
      {:else}
        <Text size="sm" family="mono" tone={i === items.length - 1 ? 'primary' : 'secondary'}>
          {crumb.label}
        </Text>
      {/if}
    {/each}
  </Stack>
</nav>
