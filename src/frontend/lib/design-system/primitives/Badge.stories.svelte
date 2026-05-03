<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Badge from './Badge.svelte';

  const { Story } = defineMeta({
    title: 'Primitives/Badge',
    component: Badge,
    tags: ['autodocs'],
    argTypes: {
      status: {
        control: { type: 'select' },
        options: ['accent', 'success', 'warning', 'danger', 'info', 'muted'],
      },
      variant: { control: { type: 'select' }, options: ['soft', 'outline'] },
      size: { control: { type: 'select' }, options: ['sm', 'md'] },
    },
  });
</script>

<Story name="All statuses">
  <div class="flex flex-wrap gap-2">
    <Badge status="accent">accent</Badge>
    <Badge status="success">success</Badge>
    <Badge status="warning">warning</Badge>
    <Badge status="danger">danger</Badge>
    <Badge status="info">info</Badge>
    <Badge status="muted">muted</Badge>
  </div>
</Story>

<Story name="Variants">
  <div class="flex flex-wrap gap-2">
    <Badge status="success" variant="soft">soft</Badge>
    <Badge status="success" variant="outline">outline</Badge>
  </div>
</Story>
