<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const stack = cva('flex', {
    variants: {
      direction: { row: 'flex-row', col: 'flex-col' },
      gap: {
        0: 'gap-0',
        1: 'gap-1',
        2: 'gap-2',
        3: 'gap-3',
        4: 'gap-4',
        6: 'gap-6',
        8: 'gap-8',
      },
      align: {
        start: 'items-start',
        center: 'items-center',
        end: 'items-end',
        stretch: 'items-stretch',
        baseline: 'items-baseline',
      },
      justify: {
        start: 'justify-start',
        center: 'justify-center',
        end: 'justify-end',
        between: 'justify-between',
        around: 'justify-around',
      },
      wrap: { true: 'flex-wrap', false: 'flex-nowrap' },
    },
    defaults: { direction: 'col', gap: 4, align: 'stretch', justify: 'start', wrap: false },
  });

  type StackVariants = CvaProps<{
    direction: { row: string; col: string };
    gap: { 0: string; 1: string; 2: string; 3: string; 4: string; 6: string; 8: string };
    align: { start: string; center: string; end: string; stretch: string; baseline: string };
    justify: { start: string; center: string; end: string; between: string; around: string };
    wrap: { true: string; false: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = StackVariants & {
    class?: string | undefined;
    'data-testid'?: string | undefined;
    children?: Snippet | undefined;
    as?: keyof HTMLElementTagNameMap | undefined;
  };

  let {
    direction = 'col',
    gap = 4,
    align = 'stretch',
    justify = 'start',
    wrap = false,
    class: extra = '',
    children,
  }: Props = $props();
</script>

<div class={stack({ direction, gap, align, justify, wrap, class: extra })}>
  {#if children}{@render children()}{/if}
</div>
