import { describe, expect, test } from 'vitest';
import { cva } from './cva.js';

describe('cva', () => {
  test('should_apply_base_class_when_no_props_passed', () => {
    const fn = cva('btn');
    expect(fn()).toBe('btn');
  });

  test('should_apply_default_variant_when_prop_omitted', () => {
    const fn = cva('btn', {
      variants: { size: { sm: 'h-8', md: 'h-10' } },
      defaults: { size: 'md' },
    });
    expect(fn()).toContain('h-10');
  });

  test('should_apply_chosen_variant_when_prop_passed', () => {
    const fn = cva('btn', {
      variants: { size: { sm: 'h-8', md: 'h-10' } },
      defaults: { size: 'md' },
    });
    expect(fn({ size: 'sm' })).toContain('h-8');
    expect(fn({ size: 'sm' })).not.toContain('h-10');
  });

  test('should_merge_extra_class_with_tailwind_conflict_resolution', () => {
    const fn = cva('btn', {
      variants: { size: { sm: 'h-8', md: 'h-10' } },
      defaults: { size: 'md' },
    });
    expect(fn({ class: 'h-12' })).toContain('h-12');
    expect(fn({ class: 'h-12' })).not.toContain('h-10');
  });

  test('should_accept_native_true_for_boolean_variant', () => {
    const fn = cva('btn', {
      variants: { block: { true: 'w-full', false: 'w-auto' } },
      defaults: { block: false },
    });
    expect(fn({ block: true })).toContain('w-full');
    expect(fn({ block: true })).not.toContain('w-auto');
  });

  test('should_accept_native_false_for_boolean_variant', () => {
    const fn = cva('btn', {
      variants: { block: { true: 'w-full', false: 'w-auto' } },
      defaults: { block: true },
    });
    expect(fn({ block: false })).toContain('w-auto');
  });

  test('should_apply_default_boolean_when_prop_omitted', () => {
    const fn = cva('btn', {
      variants: { block: { true: 'w-full', false: 'w-auto' } },
      defaults: { block: true },
    });
    expect(fn()).toContain('w-full');
  });

  test('should_apply_compound_rule_when_all_keys_match', () => {
    const fn = cva('btn', {
      variants: {
        intent: { accent: 'bg-accent', danger: 'bg-danger' },
        size: { sm: 'h-8', md: 'h-10' },
      },
      compound: [{ intent: 'danger', size: 'sm', class: 'ring-2' }],
    });
    expect(fn({ intent: 'danger', size: 'sm' })).toContain('ring-2');
    expect(fn({ intent: 'danger', size: 'md' })).not.toContain('ring-2');
  });
});
