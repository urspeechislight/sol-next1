<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const card = cva('rounded-lg border transition-colors duration-fast ease-standard', {
    variants: {
      surface: {
        1: 'bg-bg-1 border-border-1',
        2: 'bg-bg-2 border-border-1',
        elevated: 'bg-bg-1 border-border-1 shadow-md',
      },
      padding: {
        none: 'p-0',
        sm: 'p-3',
        md: 'p-5',
        lg: 'p-8',
      },
      interactive: {
        true: 'cursor-pointer hover:border-border-strong',
        false: '',
      },
    },
    defaults: { surface: 1, padding: 'md', interactive: false },
  });

  type CardVariants = CvaProps<{
    surface: { 1: string; 2: string; elevated: string };
    padding: { none: string; sm: string; md: string; lg: string };
    interactive: { true: string; false: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = CardVariants & {
    class?: string | undefined;
    'data-testid'?: string | undefined;
    children?: Snippet | undefined;
  };

  let {
    surface = 1,
    padding = 'md',
    interactive = false,
    class: extra = '',
    children,
  }: Props = $props();
</script>

<div class={card({ surface, padding, interactive, class: extra })}>
  {#if children}{@render children()}{/if}
</div>
