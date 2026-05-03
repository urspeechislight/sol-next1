/**
 * Type-safe registry of every design token defined in tokens.css.
 *
 * Why mirror the CSS in TS?
 *   - Variant maps (variants.ts) reference tokens by name; if a variant points
 *     to a token that doesn't exist, TypeScript will fail the build.
 *   - The harness (.claude/lib/handlers/tokens_only.py) reads this file to
 *     know which token names are legal.
 *
 * Rules:
 *   - Every key here MUST exist as a CSS custom property in tokens.css.
 *   - Values here are token NAMES, never raw colors / sizes — single source of
 *     truth stays in tokens.css.
 */

export const colorTokens = {
  bg: {
    0: 'var(--color-bg-0)',
    1: 'var(--color-bg-1)',
    2: 'var(--color-bg-2)',
    3: 'var(--color-bg-3)',
  },
  fg: {
    1: 'var(--color-fg-1)',
    2: 'var(--color-fg-2)',
    3: 'var(--color-fg-3)',
    onAccent: 'var(--color-fg-on-accent)',
    onDanger: 'var(--color-fg-on-danger)',
  },
  status: {
    accent: 'var(--color-accent)',
    accentStrong: 'var(--color-accent-strong)',
    accentSoft: 'var(--color-accent-soft)',
    success: 'var(--color-success)',
    successSoft: 'var(--color-success-soft)',
    warning: 'var(--color-warning)',
    warningSoft: 'var(--color-warning-soft)',
    danger: 'var(--color-danger)',
    dangerSoft: 'var(--color-danger-soft)',
    info: 'var(--color-info)',
    infoSoft: 'var(--color-info-soft)',
    muted: 'var(--color-muted)',
    mutedSoft: 'var(--color-muted-soft)',
  },
  border: {
    1: 'var(--color-border-1)',
    2: 'var(--color-border-2)',
    strong: 'var(--color-border-strong)',
  },
} as const;

export const radiusTokens = {
  xs: 'var(--radius-xs)',
  sm: 'var(--radius-sm)',
  md: 'var(--radius-md)',
  lg: 'var(--radius-lg)',
  xl: 'var(--radius-xl)',
  full: 'var(--radius-full)',
} as const;

export const shadowTokens = {
  sm: 'var(--shadow-sm)',
  md: 'var(--shadow-md)',
  lg: 'var(--shadow-lg)',
  glowAccent: 'var(--shadow-glow-accent)',
  glowDanger: 'var(--shadow-glow-danger)',
} as const;

export const typeScaleTokens = {
  xs: 'var(--text-xs)',
  sm: 'var(--text-sm)',
  base: 'var(--text-base)',
  lg: 'var(--text-lg)',
  xl: 'var(--text-xl)',
  '2xl': 'var(--text-2xl)',
  '3xl': 'var(--text-3xl)',
  '4xl': 'var(--text-4xl)',
  '5xl': 'var(--text-5xl)',
} as const;

export const motionTokens = {
  duration: {
    fast: 'var(--duration-fast)',
    normal: 'var(--duration-normal)',
    slow: 'var(--duration-slow)',
  },
  ease: {
    standard: 'var(--ease-standard)',
    emphasized: 'var(--ease-emphasized)',
    out: 'var(--ease-out)',
  },
} as const;

/* ----- Status semantic vocabulary -------------------------------------------- */

export const STATUS_KEYS = ['accent', 'success', 'warning', 'danger', 'info', 'muted'] as const;

export type StatusKey = (typeof STATUS_KEYS)[number];

export const SIZE_KEYS = ['xs', 'sm', 'md', 'lg', 'xl'] as const;
export type SizeKey = (typeof SIZE_KEYS)[number];
