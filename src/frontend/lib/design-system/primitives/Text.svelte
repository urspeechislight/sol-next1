<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const text = cva('', {
    variants: {
      size: {
        xs: 'text-xs',
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl',
        '2xl': 'text-2xl',
        '3xl': 'text-3xl',
        '4xl': 'text-4xl',
      },
      weight: {
        normal: 'font-normal',
        medium: 'font-medium',
        semibold: 'font-semibold',
        bold: 'font-bold',
      },
      tone: {
        primary: 'text-fg-1',
        secondary: 'text-fg-2',
        tertiary: 'text-fg-3',
        accent: 'text-accent',
        success: 'text-success',
        warning: 'text-warning',
        danger: 'text-danger',
        info: 'text-info',
        muted: 'text-muted',
      },
      family: {
        sans: 'font-sans',
        mono: 'font-mono',
        display: 'font-display',
      },
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
      },
      truncate: { true: 'truncate', false: '' },
    },
    defaults: {
      size: 'base',
      weight: 'normal',
      tone: 'primary',
      family: 'sans',
      align: 'left',
      truncate: false,
    },
  });

  type TextVariants = CvaProps<{
    size: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
      '4xl': string;
    };
    weight: { normal: string; medium: string; semibold: string; bold: string };
    tone: {
      primary: string;
      secondary: string;
      tertiary: string;
      accent: string;
      success: string;
      warning: string;
      danger: string;
      info: string;
      muted: string;
    };
    family: { sans: string; mono: string; display: string };
    align: { left: string; center: string; right: string };
    truncate: { true: string; false: string };
  }>;
</script>

<script lang="ts">
  import type { Snippet } from 'svelte';

  type Tag = 'p' | 'span' | 'div' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'small' | 'strong';

  type Props = TextVariants & {
    as?: Tag | undefined;
    class?: string | undefined;
    'data-testid'?: string | undefined;
    children?: Snippet | undefined;
  };

  let {
    as = 'p',
    size = 'base',
    weight = 'normal',
    tone = 'primary',
    family = 'sans',
    align = 'left',
    truncate = false,
    class: extra = '',
    children,
  }: Props = $props();

  const klass = $derived(text({ size, weight, tone, family, align, truncate, class: extra }));
</script>

<svelte:element this={as} class={klass}>
  {#if children}{@render children()}{/if}
</svelte:element>
