<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const icon = cva('inline-block shrink-0', {
    variants: {
      size: {
        xs: 'h-3 w-3',
        sm: 'h-4 w-4',
        md: 'h-5 w-5',
        lg: 'h-6 w-6',
        xl: 'h-8 w-8',
      },
      tone: {
        current: 'text-current',
        primary: 'text-fg-1',
        secondary: 'text-fg-2',
        tertiary: 'text-fg-3',
        accent: 'text-accent',
        success: 'text-success',
        warning: 'text-warning',
        danger: 'text-danger',
        info: 'text-info',
      },
    },
    defaults: { size: 'md', tone: 'current' },
  });

  type IconVariants = CvaProps<{
    size: { xs: string; sm: string; md: string; lg: string; xl: string };
    tone: {
      current: string;
      primary: string;
      secondary: string;
      tertiary: string;
      accent: string;
      success: string;
      warning: string;
      danger: string;
      info: string;
    };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = IconVariants & {
    label?: string | undefined;
    class?: string | undefined;
    children?: Snippet | undefined;
  };

  let { size = 'md', tone = 'current', label, class: extra = '', children }: Props = $props();
</script>

<span
  class={icon({ size, tone, class: extra })}
  role={label ? 'img' : 'presentation'}
  aria-label={label}
>
  {#if children}{@render children()}{/if}
</span>
