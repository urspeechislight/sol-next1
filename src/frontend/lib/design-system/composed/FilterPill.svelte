<!--
  src/frontend/lib/design-system/composed/FilterPill.svelte

  Toggleable pill used in filter rails. Active = accent-soft fill, inactive
  = transparent with border. Composes Button primitive (intent=ghost or
  intent=subtle) so all colors trace back to tokens.
-->
<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const pill = cva(
    'inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium ' +
      'border transition-colors duration-fast ease-standard cursor-pointer ' +
      'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ' +
      'focus-visible:outline-accent',
    {
      variants: {
        active: {
          true: 'bg-accent-soft text-accent border-transparent',
          false:
            'bg-transparent text-fg-2 border-border-1 hover:border-border-strong hover:text-fg-1',
        },
      },
      defaults: { active: false },
    },
  );

  type PillVariants = CvaProps<{
    active: { true: string; false: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = PillVariants & {
    onclick?: (() => void) | undefined;
    class?: string | undefined;
    children?: Snippet | undefined;
  };

  let { active = false, onclick, class: extra = '', children }: Props = $props();
</script>

<button type="button" class={pill({ active, class: extra })} {onclick}>
  {#if children}{@render children()}{/if}
</button>
