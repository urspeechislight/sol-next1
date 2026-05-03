<!--
  Bare button primitive — a ``<button>`` with no baked-in styling, only
  the focus ring and ``type="button"`` default. Use when the design calls
  for a fully custom button shape that doesn't fit ``Button``'s intent /
  size grid (eg. an entire card-sized pressable, a vertical drawer, an
  unstyled icon target).

  Why this exists: ``primitive_usage`` (DS-003) blocks raw ``<button>`` in
  feature code, and ``Button`` always applies its own layout / size base
  classes. ``Pressable`` is the SSOT escape hatch — same accessibility
  contract (real button element, focus-visible ring), zero opinion about
  appearance.
-->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLButtonAttributes } from 'svelte/elements';

  type Props = Omit<HTMLButtonAttributes, 'class' | 'style'> & {
    class?: string | undefined;
    'data-testid'?: string | undefined;
    children?: Snippet | undefined;
  };

  let { class: extra = '', children, type = 'button', ...rest }: Props = $props();
</script>

<button
  {type}
  class="focus-visible:outline-accent focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 {extra}"
  {...rest}
>
  {#if children}{@render children()}{/if}
</button>
