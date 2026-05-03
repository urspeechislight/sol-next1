/**
 * Type contracts shared by every design-system primitive.
 * These props names must be used consistently across primitives so consumers
 * have a predictable, learnable API.
 */

import type { Snippet } from 'svelte';
import type { HTMLAttributes } from 'svelte/elements';
import type { SizeKey, StatusKey } from './tokens.js';

export type { SizeKey, StatusKey };

/** Common props every primitive accepts. */
export interface BaseProps {
  /** Extra Tailwind classes — merged with primitive's own classes. */
  class?: string | undefined;
  /** Inline style is BANNED on primitives (enforced by harness). */
  style?: never;
  /** Test hook. */
  'data-testid'?: string | undefined;
  /** Optional default content slot. */
  children?: Snippet | undefined;
}

/** Props for primitives that wrap a native HTML element. */
export type ElementProps<T extends keyof HTMLElementTagNameMap> = Omit<
  HTMLAttributes<HTMLElementTagNameMap[T]>,
  'style' | 'class'
> &
  BaseProps;

/** Variant primitives get this. */
export interface VariantProps {
  status?: StatusKey;
  size?: SizeKey;
}
