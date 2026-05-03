# Design system

The design system is **the only place** visual decisions are made. Tokens define
the values; primitives consume them; composed components compose primitives;
pages compose composed components.

## Layers

```
src/frontend/lib/design-system/
├── tokens.css           ← values (CSS custom properties, Tailwind theme)
├── tokens.ts            ← typed registry of token names (no values)
├── variants.ts          ← status → palette / band → status maps
├── cn.ts                ← clsx + tailwind-merge wrapper
├── cva.ts               ← variant helper (~50 LOC, zero deps)
├── contracts.ts         ← shared prop types every primitive accepts
├── index.ts             ← public barrel
├── primitives/          ← Button, Badge, Card, Input, Stack, Text, Icon
├── composed/            ← MetricCard, HealthBadge, PageHeader
└── internal/            ← private helpers; not importable from outside
```

## Hard rules

These are enforced by `.claude/lib/handlers/`. The harness blocks writes that
violate them — fix the violation, don't bypass.

1. **Raw color literals** (`#abc`, `rgb(...)`, `hsl(...)`, `oklch(...)`,
   `oklab(...)`) only in `tokens.css` and `internal/`. Everywhere else, use a
   Tailwind utility (`bg-accent`) or a CSS variable (`var(--color-accent)`).
   Rule: `DS-001`.

2. **Inline `style="..."`** is banned in `.svelte` files. Tailwind utilities or
   Svelte's `style:--token-name={value}` directive are the only ways to adjust
   style. The latter still routes through tokens. Rule: `DS-002`.

3. **Routes & feature components** must use design-system primitives, not raw
   `<button>` / `<input>` / `<textarea>` / `<select>`. The design-system
   directory itself can use raw HTML — that's where primitives are built. Rule:
   `DS-003`.

4. **Variant maps** (status → palette, band → status, trend → glyph) live only
   in `variants.ts`. No ad-hoc `const xToY = {...}` declarations across
   components. Rule: `DS-004`.

5. **`internal/`** is private. Routes and feature code import from
   `$lib/design-system` (the public barrel). Rule: `BND-001`.

## Adding a token

1. Add the value in `tokens.css` under `@theme { ... }`. Update the
   `[data-theme="light"]` block too if it differs in light mode.
2. Mirror the name (without the value) in `tokens.ts` so JS code can reference
   it type-safely.
3. If the token represents a status, add it to `variants.ts`.
4. Run `pnpm check` — TS will fail fast if `tokens.ts` and `variants.ts` get out
   of sync.

## Adding a primitive

1. Create `primitives/<Name>.svelte`.
2. In a `<script lang="ts" module>` block, define a `cva()` config using only
   token-backed Tailwind classes (`bg-accent`, never `bg-[#5BD9C8]`).
3. Accept props that follow `contracts.ts` (`status`, `size`, `class`,
   `data-testid`, `children`). Never accept `style`.
4. Export the primitive from `primitives/index.ts`.
5. Add a `<Name>.story.svelte` for the Histoire sandbox.
6. Document any non-obvious behavior with one short comment, no docstring.

## Adding a composed component

1. Create `composed/<Name>.svelte`.
2. Compose only primitives — no raw HTML, no Tailwind raw values.
3. If it needs new tokens, add them first (above).
4. Export from `composed/index.ts`.

## Theming

Default theme is dark (`<html data-theme="dark">`). Light theme overrides are at
`[data-theme="light"]` in `tokens.css`. The user store at `lib/stores/theme.ts`
flips the attribute and persists to localStorage; the inline script in
`app.html` applies the persisted theme before paint to avoid flash.

## Tokens reference (overview)

The authoritative list is `tokens.css`. As of foundation:

- **Surfaces:** `--color-bg-0` … `--color-bg-3`
- **Text:** `--color-fg-1` (primary), `--color-fg-2` (secondary), `--color-fg-3`
  (tertiary)
- **Status:** `accent`, `success`, `warning`, `danger`, `info`, `muted`, each
  with `-soft` and (for accent) `-strong`
- **Borders:** `--color-border-1`, `--color-border-2`, `--color-border-strong`
- **Spacing:** 4px base scale, `--spacing-0` … `--spacing-32`
- **Radii:** `xs sm md lg xl full`
- **Shadows:** `sm md lg`, plus glow tokens
- **Type:** sans / mono / display families; `xs sm base lg xl 2xl 3xl 4xl 5xl`
- **Motion:** `fast/normal/slow` durations + standard/emphasized/out easings
