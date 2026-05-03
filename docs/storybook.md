# Storybook

Storybook 8 is the design-system sandbox. It renders every primitive and
composed component in isolation with live controls, theme switching, and
auto-generated docs.

## Run locally

```bash
pnpm storybook              # dev server on :6006
pnpm storybook:build        # static build into src/frontend/storybook-static/
```

## Structure

```
src/frontend/
├── .storybook/
│   ├── main.ts              # framework + addons
│   ├── preview.ts           # global decorators (theme switcher, app.css)
│   └── manager.ts           # Storybook UI customization (currently default)
└── lib/design-system/
    ├── Tokens.stories.svelte
    └── primitives/
        ├── Button.stories.svelte
        ├── Badge.stories.svelte
        └── ...
```

## Writing a story

We use **Svelte CSF** via `@storybook/addon-svelte-csf`. Stories are written
as Svelte components with a `defineMeta` script block:

```svelte
<script context="module" lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import MyComponent from './MyComponent.svelte';

  const { Story } = defineMeta({
    title: 'Primitives/MyComponent',
    component: MyComponent,
    tags: ['autodocs'],
    argTypes: { /* live controls */ },
  });
</script>

<Story name="Default" args={{ ... }}>
  {#snippet template(args)}
    <MyComponent {...args}>content</MyComponent>
  {/snippet}
</Story>
```

## Theme switcher

`@storybook/addon-themes` flips `data-theme` on the iframe root, exactly the
way the app does it. The token system reacts automatically.

## Conventions

- One `.stories.svelte` per primitive, sitting next to the component.
- Title structure: `Tokens/...`, `Primitives/...`, `Composed/...` — keeps the
  Storybook nav grouped by design-system layer.
- Always include an `Intents` or `Variants` story showing every option side-by-side.
- Tag with `'autodocs'` for components — Storybook auto-builds a docs page.

## Why Storybook over Histoire

- **Svelte 5 support** is currently more reliable in Storybook 8 + Svelte CSF v4.
- Mature ecosystem of addons (a11y, interactions, themes, viewport).
- Auto-generated `argTypes` from TS prop types when supported.

The trade-off is bundle size — Storybook adds ~50 MB of dev dependencies,
but it doesn't ship to production.
