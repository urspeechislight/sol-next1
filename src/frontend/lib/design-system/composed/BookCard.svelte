<!--
  src/frontend/lib/design-system/composed/BookCard.svelte

  Single source of truth for how a book entity is displayed in lists/grids.
  Two layouts share one type system — `row` (dense, full-bleed editorial row)
  and `card` (compact grid card).

  Composes only primitives + sect/canonical badges. No raw colors, no inline
  styles. Hard rules DS-001 / DS-002 / DS-004 satisfied.
-->
<script lang="ts" module>
  import { cva, type CvaProps } from '../cva.js';

  const root = cva(
    'group rounded-md border border-border-1 bg-bg-1 transition-colors ' +
      'duration-fast ease-standard hover:border-border-strong cursor-pointer',
    {
      variants: {
        layout: {
          row: 'grid grid-cols-[1fr_auto] gap-4 p-4',
          card: 'flex flex-col gap-3 p-4',
        },
      },
      defaults: { layout: 'card' },
    },
  );

  type RootVariants = CvaProps<{
    layout: { row: string; card: string };
  }>;
</script>

<script lang="ts">
  import Stack from '../primitives/Stack.svelte';
  import Text from '../primitives/Text.svelte';
  import SectBadge from './SectBadge.svelte';
  import CanonicalBadge from './CanonicalBadge.svelte';
  import type { Sect, CanonicalTier } from '../variants.js';

  interface Book {
    urn: string;
    titleArabic: string;
    titleLatin?: string | undefined;
    author?: string | undefined;
    authorAh?: number | undefined; // death date in AH
    pages?: number | undefined;
    sect: Sect;
    canonical?: CanonicalTier | undefined;
  }

  type Props = RootVariants & {
    book: Book;
    onSelect?: ((urn: string) => void) | undefined;
    class?: string | undefined;
  };

  let { book, layout = 'card', onSelect, class: extra = '' }: Props = $props();

  const klass = $derived(root({ layout, class: extra }));
  const meta = $derived(
    [
      book.author,
      book.authorAh ? `d. ${book.authorAh} AH` : null,
      book.pages ? `${book.pages} pp.` : null,
    ]
      .filter(Boolean)
      .join(' · '),
  );
</script>

<button type="button" class={klass} onclick={() => onSelect?.(book.urn)}>
  <Stack gap={2} align="start">
    <Text as="h3" size="xl" weight="semibold" family="display" align="right" class="tracking-tight">
      {book.titleArabic}
    </Text>
    {#if book.titleLatin}
      <Text size="sm" tone="secondary" class="italic">{book.titleLatin}</Text>
    {/if}
    {#if meta}
      <Text size="xs" tone="tertiary" family="mono">{meta}</Text>
    {/if}
  </Stack>

  <Stack direction={layout === 'row' ? 'col' : 'row'} gap={2} align="end" wrap>
    <SectBadge sect={book.sect} />
    {#if book.canonical}
      <CanonicalBadge tier={book.canonical} />
    {/if}
  </Stack>
</button>
