<script lang="ts">
  import '../app.css';
  import type { Snippet } from 'svelte';
  import { Stack, Text, Button } from '$lib/design-system';
  import { theme } from '$lib/stores';

  let { children }: { children: Snippet } = $props();
</script>

<div class="min-h-screen flex flex-col">
  <header
    class="border-b border-border-1 bg-bg-1/80 backdrop-blur supports-[backdrop-filter]:bg-bg-1/60"
  >
    <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
      <Stack direction="row" gap={3} align="center">
        <div
          class="h-8 w-8 rounded-md bg-accent text-fg-on-accent flex items-center justify-center font-bold"
          aria-hidden="true"
        >
          ▲
        </div>
        <Text size="lg" weight="semibold" family="display">sol-next1</Text>
      </Stack>
      <Button intent="ghost" size="sm" onclick={() => theme.toggle()}>
        Toggle theme
      </Button>
    </div>
  </header>

  <main class="flex-1 max-w-7xl mx-auto w-full px-6 py-10">
    {@render children()}
  </main>

  <footer class="border-t border-border-1">
    <div class="max-w-7xl mx-auto px-6 py-6">
      <Text size="sm" tone="tertiary">
        Built on the sol-next1 harness · design tokens are SSOT · raw colors are blocked
      </Text>
    </div>
  </footer>
</div>
