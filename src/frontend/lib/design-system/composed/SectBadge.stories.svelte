<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import SectBadge from './SectBadge.svelte';

  const { Story } = defineMeta({
    title: 'Composed/SectBadge',
    component: SectBadge,
    tags: ['autodocs'],
    argTypes: {
      sect: {
        control: { type: 'select' },
        options: ['imami', 'sunni', 'zaidi', 'ismaili', 'unknown'],
      },
      variant: { control: { type: 'select' }, options: ['soft', 'outline'] },
      size: { control: { type: 'select' }, options: ['sm', 'md'] },
    },
  });
</script>

<Story name="All sects">
  <div class="flex flex-wrap gap-2">
    <SectBadge sect="imami" />
    <SectBadge sect="sunni" />
    <SectBadge sect="zaidi" />
    <SectBadge sect="ismaili" />
    <SectBadge sect="unknown" />
  </div>
</Story>

<Story name="Soft variant">
  <div class="flex flex-wrap gap-2">
    <SectBadge sect="imami" variant="soft" />
    <SectBadge sect="sunni" variant="soft" />
    <SectBadge sect="zaidi" variant="soft" />
    <SectBadge sect="ismaili" variant="soft" />
    <SectBadge sect="unknown" variant="soft" />
  </div>
</Story>
