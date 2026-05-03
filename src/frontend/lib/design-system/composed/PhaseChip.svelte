<!--
  src/frontend/lib/design-system/composed/PhaseChip.svelte

  Pipeline phase indicator (e.g. footer ingest progress). Status mapping
  lives in variants.ts (ingestPhaseToStatus) so any future re-coloring of
  pipeline states happens in one place.
-->
<script lang="ts">
  import Badge from '../primitives/Badge.svelte';
  import { ingestPhaseToStatus, type IngestPhaseStatus } from '../variants.js';

  interface Props {
    n: number;
    label: string;
    status: IngestPhaseStatus;
    class?: string | undefined;
  }

  let { n, label, status: phaseStatus, class: extra = '' }: Props = $props();

  const status = $derived(ingestPhaseToStatus[phaseStatus]);
</script>

<Badge {status} variant="soft" size="sm" class={extra}>
  <span class="font-mono">{n}</span>
  <span aria-hidden="true">·</span>
  <span>{label}</span>
</Badge>
