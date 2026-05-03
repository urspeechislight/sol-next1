<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const button = cva(
    'inline-flex items-center justify-center gap-2 font-medium ' +
      'transition-[background,box-shadow,transform] duration-fast ease-standard ' +
      'rounded-md disabled:opacity-50 disabled:pointer-events-none ' +
      'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ' +
      'focus-visible:outline-accent select-none',
    {
      variants: {
        intent: {
          accent: 'bg-accent text-fg-on-accent hover:bg-accent-strong',
          danger: 'bg-danger text-fg-on-danger hover:opacity-90',
          ghost: 'bg-transparent text-fg-1 hover:bg-bg-2',
          outline: 'border border-border-2 text-fg-1 hover:bg-bg-2 hover:border-border-strong',
          subtle: 'bg-bg-2 text-fg-1 hover:bg-bg-3',
        },
        size: {
          sm: 'h-8 px-3 text-sm',
          md: 'h-10 px-4 text-base',
          lg: 'h-12 px-5 text-lg',
        },
        block: { true: 'w-full', false: '' },
      },
      defaults: { intent: 'accent', size: 'md', block: false },
    },
  );

  type ButtonVariants = CvaProps<{
    intent: { accent: string; danger: string; ghost: string; outline: string; subtle: string };
    size: { sm: string; md: string; lg: string };
    block: { true: string; false: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLButtonAttributes } from 'svelte/elements';

  type Props = Omit<HTMLButtonAttributes, 'class' | 'style'> &
    ButtonVariants & {
      class?: string | undefined;
      'data-testid'?: string | undefined;
      children?: Snippet | undefined;
    };

  let {
    intent = 'accent',
    size = 'md',
    block = false,
    class: extra = '',
    children,
    type = 'button',
    ...rest
  }: Props = $props();
</script>

<button {type} class={button({ intent, size, block, class: extra })} {...rest}>
  {#if children}{@render children()}{/if}
</button>
