<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const input = cva(
    'w-full rounded-md border bg-bg-1 text-fg-1 placeholder:text-fg-3 ' +
      'transition-colors duration-fast ease-standard ' +
      'focus:border-accent focus:outline-none ' +
      'disabled:opacity-50 disabled:cursor-not-allowed',
    {
      variants: {
        size: {
          sm: 'h-8 px-3 text-sm',
          md: 'h-10 px-3 text-base',
          lg: 'h-12 px-4 text-lg',
        },
        state: {
          default: 'border-border-2',
          error: 'border-danger',
          success: 'border-success',
        },
      },
      defaults: { size: 'md', state: 'default' },
    },
  );

  type InputVariants = CvaProps<{
    size: { sm: string; md: string; lg: string };
    state: { default: string; error: string; success: string };
  }>;
</script>

<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements';

  type Props = Omit<HTMLInputAttributes, 'class' | 'style' | 'size'> &
    InputVariants & {
      class?: string | undefined;
      'data-testid'?: string | undefined;
    };

  let {
    size = 'md',
    state = 'default',
    class: extra = '',
    type = 'text',
    value = $bindable<HTMLInputAttributes['value']>(),
    ...rest
  }: Props = $props();
</script>

<input {type} bind:value class={input({ size, state, class: extra })} {...rest} />
