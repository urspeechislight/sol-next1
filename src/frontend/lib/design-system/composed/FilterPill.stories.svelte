<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import FilterPill from './FilterPill.svelte';

  const { Story } = defineMeta({
    title: 'Composed/FilterPill',
    component: FilterPill,
    tags: ['autodocs'],
    argTypes: {
      active: { control: { type: 'boolean' } },
    },
  });

  let activeIndex = $state(0);
  const filters = ['All', 'Imami', 'Sunni', 'Zaidi', 'Ismaili'];
</script>

<Story name="States">
  <div class="flex flex-wrap gap-2">
    <FilterPill>Inactive</FilterPill>
    <FilterPill active>Active</FilterPill>
  </div>
</Story>

<Story name="Filter rail (interactive)">
  <div class="flex flex-wrap gap-2">
    {#each filters as f, i (f)}
      <FilterPill active={i === activeIndex} onclick={() => (activeIndex = i)}>
        {f}
      </FilterPill>
    {/each}
  </div>
</Story>
