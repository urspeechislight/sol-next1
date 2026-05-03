<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';

  const { Story } = defineMeta({
    title: 'Tokens/Overview',
    parameters: { layout: 'padded' },
  });
</script>

<script lang="ts">
  import Stack from './primitives/Stack.svelte';
  import Text from './primitives/Text.svelte';

  const surfaces = ['bg-0', 'bg-1', 'bg-2', 'bg-3'] as const;
  const statuses = ['accent', 'success', 'warning', 'danger', 'info', 'muted'] as const;
  const radii = ['xs', 'sm', 'md', 'lg', 'xl'] as const;
</script>

<Story name="Surfaces">
  <div class="grid grid-cols-4 gap-3">
    {#each surfaces as s}
      <div
        class="rounded-md p-6 border border-border-1"
        style:background={`var(--color-${s})`}
      >
        <Text size="sm" family="mono">{s}</Text>
      </div>
    {/each}
  </div>
</Story>

<Story name="Status colors">
  <div class="grid grid-cols-3 gap-3">
    {#each statuses as s}
      <div class="rounded-md p-4 bg-bg-1 border border-border-1">
        <Stack direction="row" gap={3} align="center">
          <span class="h-8 w-8 rounded-full" style:background={`var(--color-${s})`}></span>
          <Text family="mono" size="sm">{s}</Text>
        </Stack>
      </div>
    {/each}
  </div>
</Story>

<Story name="Radii">
  <div class="grid grid-cols-5 gap-3">
    {#each radii as r}
      <div
        class="bg-bg-2 p-6 border border-border-1"
        style:border-radius={`var(--radius-${r})`}
      >
        <Text family="mono" size="sm">{r}</Text>
      </div>
    {/each}
  </div>
</Story>
