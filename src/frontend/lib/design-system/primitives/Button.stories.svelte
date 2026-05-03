<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Button from './Button.svelte';

  const { Story } = defineMeta({
    title: 'Primitives/Button',
    component: Button,
    tags: ['autodocs'],
    argTypes: {
      intent: {
        control: { type: 'select' },
        options: ['accent', 'danger', 'ghost', 'outline', 'subtle'],
      },
      size: { control: { type: 'select' }, options: ['sm', 'md', 'lg'] },
      block: { control: { type: 'boolean' } },
      disabled: { control: { type: 'boolean' } },
    },
  });
</script>

<Story name="Default" args={{ intent: 'accent', size: 'md' }}>
  {#snippet template(args)}
    <Button {...args}>Click me</Button>
  {/snippet}
</Story>

<Story name="Intents">
  <div class="flex flex-wrap gap-3">
    <Button intent="accent">Accent</Button>
    <Button intent="subtle">Subtle</Button>
    <Button intent="outline">Outline</Button>
    <Button intent="ghost">Ghost</Button>
    <Button intent="danger">Danger</Button>
  </div>
</Story>

<Story name="Sizes">
  <div class="flex items-center gap-3">
    <Button size="sm">Small</Button>
    <Button size="md">Medium</Button>
    <Button size="lg">Large</Button>
  </div>
</Story>

<Story name="States">
  <div class="flex gap-3">
    <Button>Default</Button>
    <Button disabled>Disabled</Button>
    <Button block>Block</Button>
  </div>
</Story>
