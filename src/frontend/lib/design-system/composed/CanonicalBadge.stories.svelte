<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import CanonicalBadge from './CanonicalBadge.svelte';

  const { Story } = defineMeta({
    title: 'Composed/CanonicalBadge',
    component: CanonicalBadge,
    tags: ['autodocs'],
    argTypes: {
      tier: {
        control: { type: 'select' },
        options: ['primary', 'secondary', 'commentary', 'reference'],
      },
      variant: { control: { type: 'select' }, options: ['soft', 'outline'] },
      size: { control: { type: 'select' }, options: ['sm', 'md'] },
    },
  });
</script>

<Story name="All tiers">
  <div class="flex flex-wrap gap-2">
    <CanonicalBadge tier="primary" />
    <CanonicalBadge tier="secondary" />
    <CanonicalBadge tier="commentary" />
    <CanonicalBadge tier="reference" />
  </div>
</Story>

<Story name="Outline variant">
  <div class="flex flex-wrap gap-2">
    <CanonicalBadge tier="primary" variant="outline" />
    <CanonicalBadge tier="secondary" variant="outline" />
    <CanonicalBadge tier="commentary" variant="outline" />
    <CanonicalBadge tier="reference" variant="outline" />
  </div>
</Story>
