<!--
  Domain cabinet — seven vertical drawers, click-to-pin to expand a tray
  beneath the active column. Hover gives a transient preview; clicking
  again or pressing Escape closes the pinned drawer.

  Visually echoes the design prototype's "card catalog" metaphor but
  composes design-system tokens (no raw colors, no inline styles).
  Decorative motion details from the prototype (gold halo glow,
  starfield backing, animated handle pulls) are intentionally omitted
  here in favor of tasteful, token-clean states; they can be layered
  on as a follow-up once the structural port lands.
-->
<script lang="ts">
  import { goto } from '$app/navigation';
  import { Pressable, Stack, Text } from '$lib/design-system';
  import { DOMAINS } from '$lib/fixtures';
  import DomainGlyph from './DomainGlyph.svelte';

  let pinned = $state<number | null>(null);
  let hover = $state<number | null>(null);
  const active = $derived(hover ?? pinned);
  const activeDomain = $derived(active != null ? (DOMAINS[active] ?? null) : null);
  const totalWorks = $derived(
    DOMAINS.reduce((a, d) => a + d.categories.reduce((aa, c) => aa + c.count, 0), 0),
  );

  let cabinetEl: HTMLElement | undefined = $state();

  $effect(() => {
    if (pinned == null) return;
    function onDoc(e: MouseEvent) {
      if (cabinetEl && !cabinetEl.contains(e.target as Node)) pinned = null;
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') pinned = null;
    }
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDoc);
      document.removeEventListener('keydown', onKey);
    };
  });

  function pin(i: number) {
    pinned = pinned === i ? null : i;
  }

  function go(slug: string) {
    void goto(`/library/${slug}`);
  }
</script>

<section bind:this={cabinetEl} class="cabinet" aria-labelledby="cabinet-head">
  <header class="border-border-1 mb-4 flex flex-wrap items-baseline gap-6 border-b pb-4">
    <Text size="xs" family="mono" tone="accent" class="uppercase tracking-widest">§ I</Text>
    <h2
      id="cabinet-head"
      class="text-fg-1 font-display m-0 flex-1 text-2xl font-medium tracking-tight"
    >
      <em class="text-accent font-normal italic">Domains</em> of Knowledge
    </h2>
    <Stack direction="row" gap={1} align="baseline">
      <Text family="mono" size="xs" tone="tertiary" class="uppercase tracking-widest">
        {DOMAINS.length} domains · {totalWorks} works
      </Text>
    </Stack>
  </header>

  <div
    class="border-border-1 bg-border-1 grid grid-cols-7 gap-px overflow-visible rounded border"
    role="tablist"
    aria-label="Domains of Knowledge"
  >
    {#each DOMAINS as d, i (d.id)}
      {@const works = d.categories.reduce((a, c) => a + c.count, 0)}
      {@const num = String(i + 1).padStart(2, '0')}
      <Pressable
        class="drawer {active === i ? 'active' : ''} {active != null && active !== i ? 'dim' : ''}"
        role="tab"
        aria-selected={pinned === i}
        aria-label={`${d.label} — ${works} works`}
        onmouseenter={() => (hover = i)}
        onmouseleave={() => (hover = null)}
        onfocus={() => (hover = i)}
        onblur={() => (hover = null)}
        onclick={() => pin(i)}
      >
        <span class="drawer__ar" dir="rtl">{d.labelAr}</span>
        <span class="text-accent flex h-12 w-12 items-center justify-center">
          <DomainGlyph id={d.id} size={48} />
        </span>
        <span class="bg-border-1 my-2 h-px w-full" aria-hidden="true"></span>
        <span class="flex flex-col items-center gap-0.5 px-1 text-center">
          <Text family="mono" size="xs" tone="tertiary" class="tracking-widest">{num}</Text>
          <Text size="sm" family="display" class="text-fg-1 italic">{d.label}</Text>
          <Text family="mono" size="xs" tone="accent">{works}</Text>
        </span>
      </Pressable>
    {/each}
  </div>

  {#if activeDomain && active != null}
    {@const d = activeDomain}
    {@const works = d.categories.reduce((a, c) => a + c.count, 0)}
    <div
      class="border-border-1 bg-bg-1 mt-px overflow-hidden rounded-b border border-t-0 px-7 pb-7 pt-7 shadow-md"
      role="tabpanel"
    >
      <Stack direction="row" gap={6} align="start" justify="between" wrap class="mb-5">
        <Stack gap={2}>
          <Text family="mono" size="xs" tone="accent" class="uppercase tracking-widest">
            § {String(active + 1).padStart(2, '0')}
          </Text>
          <Text as="h3" size="2xl" weight="medium" family="display" class="tracking-tight">
            {d.label}
            <span class="text-accent ms-2" dir="rtl">· {d.labelAr}</span>
          </Text>
          <Text size="sm" tone="secondary" class="max-w-2xl">{d.blurb}</Text>
        </Stack>
        <Stack direction="row" gap={6}>
          <Stack gap={1} align="end">
            <Text family="display" size="2xl" class="text-accent italic">{works}</Text>
            <Text family="mono" size="xs" tone="tertiary" class="uppercase tracking-wide"
              >works</Text
            >
          </Stack>
          <Stack gap={1} align="end">
            <Text family="display" size="2xl" class="text-accent italic">{d.categories.length}</Text
            >
            <Text family="mono" size="xs" tone="tertiary" class="uppercase tracking-wide"
              >categories</Text
            >
          </Stack>
          {#if pinned === active}
            <Pressable
              class="text-fg-3 hover:text-fg-1 transition-colors"
              aria-label="Close drawer"
              onclick={(e: MouseEvent) => {
                e.stopPropagation();
                pinned = null;
              }}
            >
              ✕
            </Pressable>
          {/if}
        </Stack>
      </Stack>

      <div class="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {#each d.categories as c, ci (c.slug)}
          <Pressable
            class="cat border-border-1 hover:bg-bg-2 hover:border-border-strong group flex items-center gap-3 rounded border p-3 text-left transition-colors"
            onclick={(e: MouseEvent) => {
              e.stopPropagation();
              go(c.slug);
            }}
          >
            <Text family="mono" size="xs" tone="tertiary" class="tracking-widest"
              >{String(ci + 1).padStart(2, '0')}</Text
            >
            <Stack gap={0} class="min-w-0 flex-1">
              <Text size="sm" class="text-fg-1 truncate">{c.label}</Text>
              <span class="text-fg-3 truncate text-xs" dir="rtl">{c.labelAr}</span>
            </Stack>
            <Text family="mono" size="xs" tone="accent">{c.count}</Text>
            <span class="text-fg-3 group-hover:text-accent transition-colors" aria-hidden="true"
              >→</span
            >
          </Pressable>
        {/each}
      </div>
    </div>
  {/if}
</section>

<style>
  .cabinet {
    position: relative;
    z-index: 1;
  }

  /* Each drawer is rendered by the Pressable primitive, so scoped Svelte
     CSS won't match — :global() selectors apply to the button element our
     parent emits. Layout uses a grid of fixed top/bottom rows with a
     flexible centre so glyph + arabic caption stay aligned across the
     seven columns. */
  :global(.drawer) {
    cursor: pointer;
    background: var(--color-bg-1);
    color: var(--color-fg-2);
    display: grid;
    grid-template-rows: 1fr auto auto auto;
    align-items: center;
    justify-items: center;
    min-height: 220px;
    padding: 14px 6px 14px;
    border: none;
    transition:
      background var(--duration-normal) var(--ease-standard),
      color var(--duration-normal) var(--ease-standard);
  }
  :global(.drawer:first-of-type) {
    border-top-left-radius: var(--radius-xs);
    border-bottom-left-radius: var(--radius-xs);
  }
  :global(.drawer:last-of-type) {
    border-top-right-radius: var(--radius-xs);
    border-bottom-right-radius: var(--radius-xs);
  }
  :global(.drawer:hover) {
    background: var(--color-bg-2);
    color: var(--color-fg-1);
  }
  :global(.drawer.active) {
    background: var(--color-accent-soft);
    color: var(--color-fg-1);
  }
  :global(.drawer.dim) {
    opacity: 0.5;
  }

  /* Vertical Arabic caption — written top-to-bottom, mixed orientation. */
  :global(.drawer__ar) {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-family: var(--font-arabic);
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--color-accent);
    line-height: 1.2;
    padding: 8px 0;
    transition: color var(--duration-normal) var(--ease-standard);
  }
  :global(.drawer.active .drawer__ar) {
    color: var(--color-fg-1);
  }
</style>
