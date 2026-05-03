# ADR 0002 — Design tokens are the single source of truth

**Date:** 2026-05-02
**Status:** Accepted

## Context

A typical app accumulates design decisions in many places: ad-hoc colors in
components, font sizes copy-pasted from Figma, inline styles applied because
"it's just this one place." Over time the visual vocabulary fragments and
"rebrand the app" becomes a multi-week refactor.

## Decision

- One file (`src/frontend/lib/design-system/tokens.css`) defines every visual
  value: colors, type scale, spacing, radii, shadows, motion. Everything is
  CSS custom properties exposed as Tailwind 4 theme tokens via `@theme`.
- A type-safe registry (`tokens.ts`) mirrors token *names* (not values) so
  TypeScript code can reference tokens with autocomplete and break the build
  when a token name disappears.
- Status / band / trend → token mappings live in `variants.ts`. Components
  import from there, never declare inline.
- The harness enforces all of the above with `block`-severity hooks. Raw
  hex / `rgb()` / `oklch()` literals outside `tokens.css` are blocked.
  Inline `style="..."` is blocked. Routes using raw `<button>`/`<input>` are
  blocked.

## Consequences

**Positive**

- "Rebrand the app" = edit one file.
- Consistent visual vocabulary across every contributor (human and agent).
- The harness catches drift the moment it's typed, not at code review.

**Negative**

- Higher up-front cost when adding a new visual property (must add token
  first, then reference it). This is the entire point — the friction is
  what produces the consistency.
- Strict rules can frustrate contributors not used to a design-system-first
  workflow. Mitigated by clear block messages that link to
  `docs/design-system.md`.

## Alternatives considered

- **Tailwind 3 + extending `theme.extend`**: works but lives in JS config;
  light/dark switching is messier; harder to consume from non-Tailwind code.
- **CSS-in-JS (e.g., emotion / vanilla-extract)**: overkill for this stack
  and conflicts with Tailwind 4's design philosophy.
- **Just discipline, no enforcement**: tried elsewhere; entropy wins.
