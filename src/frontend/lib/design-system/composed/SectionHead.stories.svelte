<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import SectionHead from './SectionHead.svelte';

  const { Story } = defineMeta({
    title: 'Composed/SectionHead',
    component: SectionHead,
    tags: ['autodocs'],
  });
</script>

<Story name="Title only">
  <SectionHead title="Foundational Works" />
</Story>

<Story name="With eyebrow">
  <SectionHead eyebrow="§ I" title="Domain Constellations" />
</Story>

<Story name="With actions">
  {#snippet template()}
    <SectionHead eyebrow="Section II" title="Reading Room">
      {#snippet actions()}
        <a href="/library" class="text-fg-2 hover:text-fg-1 font-mono text-sm">View all →</a>
      {/snippet}
    </SectionHead>
  {/snippet}
</Story>
