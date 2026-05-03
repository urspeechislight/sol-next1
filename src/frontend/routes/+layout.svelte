<script lang="ts">
  import '../app.css';
  import type { Snippet } from 'svelte';
  import { Stack, Text, Button } from '$lib/design-system';
  import { theme } from '$lib/stores';

  let { children }: { children: Snippet } = $props();
</script>

<div class="flex min-h-screen flex-col">
  <header
    class="border-border-1 bg-bg-1/80 supports-[backdrop-filter]:bg-bg-1/60 border-b backdrop-blur"
  >
    <div class="mx-auto flex h-14 max-w-7xl items-center justify-between px-6">
      <Stack direction="row" gap={3} align="center">
        <div
          class="bg-accent text-fg-on-accent flex h-8 w-8 items-center justify-center rounded-md font-bold"
          aria-hidden="true"
        >
          ▲
        </div>
        <Text size="lg" weight="semibold" family="display">sol-next1</Text>
      </Stack>
      <Button intent="ghost" size="sm" onclick={() => theme.toggle()}>Toggle theme</Button>
    </div>
  </header>

  <main class="mx-auto w-full max-w-7xl flex-1 px-6 py-10">
    {@render children()}
  </main>

  <footer class="border-border-1 border-t">
    <div class="mx-auto max-w-7xl px-6 py-6">
      <Text size="sm" tone="tertiary">
        Built on the sol-next1 harness · design tokens are SSOT · raw colors are blocked
      </Text>
    </div>
  </footer>
</div>
