/**
 * Tiny variants helper modeled after class-variance-authority. We ship our own
 * so the design system has zero runtime dependencies beyond clsx + tailwind-merge.
 *
 * Usage:
 *   const button = cva('btn-base', {
 *     variants: {
 *       intent: { accent: 'bg-accent text-fg-on-accent', danger: 'bg-danger text-fg-on-danger' },
 *       size:   { sm: 'h-8 px-3 text-sm', md: 'h-10 px-4 text-base' },
 *       block:  { true: 'w-full', false: '' },     // ← boolean variant
 *     },
 *     defaults: { intent: 'accent', size: 'md', block: false },
 *   });
 *
 *   button({ intent: 'danger', size: 'sm', block: true, class: 'mt-2' });
 *
 * Boolean coercion:
 *   When a variant has both `true` and `false` keys, props accept native
 *   booleans. The runtime coerces `true` → `'true'` and `false` → `'false'`
 *   for lookup. This lets consumers write `<Button block />` (boolean
 *   shorthand) instead of `<Button block="true" />`.
 */

import { cn } from './cn.js';

type VariantKey = string;
type VariantValue = string;
type VariantMap = Record<VariantKey, Record<VariantValue, string>>;

/** True if the variant has both `true` and `false` keys (a boolean variant). */
type IsBooleanVariant<V> = 'true' extends keyof V ? ('false' extends keyof V ? true : false) : false;

/**
 * Prop type for one variant key. Boolean variants accept `boolean | 'true' | 'false'`;
 * other variants accept their literal keys.
 */
type CvaPropValue<V> = IsBooleanVariant<V> extends true ? boolean | 'true' | 'false' : keyof V;

type VariantProps<V extends VariantMap> = {
  [K in keyof V]?: CvaPropValue<V[K]>;
};

export interface CvaConfig<V extends VariantMap> {
  variants?: V;
  defaults?: VariantProps<V>;
  compound?: Array<VariantProps<V> & { class: string }>;
}

export type CvaProps<V extends VariantMap> = VariantProps<V> & {
  class?: string | undefined;
};

/** Coerce booleans → 'true'/'false' string keys for variant lookup. */
function coerceKey(value: unknown): string | undefined {
  if (value === undefined || value === null) return undefined;
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  return String(value);
}

export function cva<V extends VariantMap>(base: string, config: CvaConfig<V> = {}) {
  const { variants, defaults, compound } = config;

  return (props: CvaProps<V> = {}): string => {
    const classes: string[] = [base];

    if (variants) {
      for (const key of Object.keys(variants) as Array<keyof V>) {
        const chosen = props[key] ?? defaults?.[key];
        const lookupKey = coerceKey(chosen);
        if (lookupKey !== undefined) {
          const variantClass = variants[key]?.[lookupKey];
          if (variantClass) classes.push(variantClass);
        }
      }
    }

    if (compound) {
      for (const rule of compound) {
        const { class: extra, ...match } = rule;
        const allMatch = (Object.keys(match) as Array<keyof V>).every((k) => {
          const want = coerceKey(match[k]);
          const got = coerceKey(props[k] ?? defaults?.[k]);
          return want === got;
        });
        if (allMatch) classes.push(extra);
      }
    }

    return cn(...classes, props.class);
  };
}
