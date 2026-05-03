<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const badge = cva(
    'inline-flex items-center gap-1 rounded-full font-medium border ' +
      'whitespace-nowrap leading-tight tracking-tight',
    {
      variants: {
        status: {
          accent: 'text-accent bg-accent-soft border-transparent',
          success: 'text-success bg-success-soft border-transparent',
          warning: 'text-warning bg-warning-soft border-transparent',
          danger: 'text-danger bg-danger-soft border-transparent',
          info: 'text-info bg-info-soft border-transparent',
          muted: 'text-fg-2 bg-muted-soft border-transparent',
        },
        variant: {
          soft: '',
          outline: 'bg-transparent border-current',
        },
        size: {
          sm: 'text-xs px-2 py-0.5',
          md: 'text-sm px-2.5 py-1',
        },
      },
      defaults: { status: 'muted', variant: 'soft', size: 'sm' },
    },
  );

  type BadgeVariants = CvaProps<{
    status: {
      accent: string;
      success: string;
      warning: string;
      danger: string;
      info: string;
      muted: string;
    };
    variant: { soft: string; outline: string };
    size: { sm: string; md: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Props = BadgeVariants & {
    class?: string | undefined;
    'data-testid'?: string | undefined;
    children?: Snippet | undefined;
  };

  let {
    status = 'muted',
    variant = 'soft',
    size = 'sm',
    class: extra = '',
    children,
  }: Props = $props();
</script>

<span class={badge({ status, variant, size, class: extra })}>
  {#if children}{@render children()}{/if}
</span>
