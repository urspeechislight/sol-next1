<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import PhaseChip from './PhaseChip.svelte';

  const { Story } = defineMeta({
    title: 'Composed/PhaseChip',
    component: PhaseChip,
    tags: ['autodocs'],
    argTypes: {
      status: {
        control: { type: 'select' },
        options: ['active', 'next', 'planned', 'done'],
      },
    },
  });
</script>

<Story name="All phases">
  <div class="flex flex-wrap gap-2">
    <PhaseChip n={1} label="ingest" status="done" />
    <PhaseChip n={2} label="segment" status="active" />
    <PhaseChip n={3} label="link" status="next" />
    <PhaseChip n={4} label="publish" status="planned" />
  </div>
</Story>

<Story name="Pipeline strip">
  <div class="flex flex-wrap gap-1">
    <PhaseChip n={1} label="acquire" status="done" />
    <PhaseChip n={2} label="ocr" status="done" />
    <PhaseChip n={3} label="segment" status="active" />
    <PhaseChip n={4} label="parse isnad" status="next" />
    <PhaseChip n={5} label="link parallels" status="planned" />
    <PhaseChip n={6} label="publish" status="planned" />
  </div>
</Story>
