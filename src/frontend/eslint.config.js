import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import prettier from 'eslint-config-prettier';
import globals from 'globals';
import ts from 'typescript-eslint';

/** @type {import('eslint').Linter.Config[]} */
export default [
  js.configs.recommended,
  ...ts.configs.recommendedTypeChecked,
  ...ts.configs.stylisticTypeChecked,
  ...svelte.configs['flat/recommended'],
  prettier,
  ...svelte.configs['flat/prettier'],
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        projectService: true,
        extraFileExtensions: ['.svelte'],
      },
    },
  },
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parserOptions: {
        parser: ts.parser,
      },
    },
  },
  {
    rules: {
      // Enforce design-system discipline at lint level (the harness blocks the rest).
      'no-restricted-syntax': [
        'error',
        {
          selector: 'Literal[value=/^#[0-9a-fA-F]{3,8}$/]',
          message:
            'Hex color literals are forbidden outside lib/design-system/tokens.css. Use a token (e.g. var(--color-accent)) instead.',
        },
      ],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      '@typescript-eslint/consistent-type-imports': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
  {
    files: ['lib/design-system/tokens.{css,ts}', 'lib/design-system/internal/**'],
    rules: {
      // The token files ARE the SSOT, so they may contain raw color values.
      'no-restricted-syntax': 'off',
    },
  },
  {
    files: ['**/*.test.ts', '**/*.spec.ts', '**/*.story.svelte'],
    rules: {
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
    },
  },
  {
    // Design-system primitives wrap an HTML element and intentionally
    // pass arbitrary HTML attributes through via ...rest. The Svelte
    // custom-element warning doesn't apply (these aren't custom elements),
    // and HTMLAttributes contains untyped event handlers that trigger
    // no-unsafe-assignment on the destructuring.
    files: ['lib/design-system/primitives/**/*.svelte'],
    rules: {
      'svelte/valid-compile': ['error', { ignoreWarnings: true }],
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },
  {
    // Config files, test setup, and SvelteKit hooks live outside the
    // type-checked source tree. Disable type-aware rules for them so
    // eslint can lint without requiring them to be in tsconfig.json's
    // project.
    files: [
      '.storybook/**/*.ts',
      'e2e/**/*.ts',
      'hooks.client.ts',
      'hooks.server.ts',
      'app.d.ts',
      'vitest-setup.ts',
      '**/*.config.{ts,js}',
      'eslint.config.js',
      'svelte.config.js',
      'playwright.config.ts',
    ],
    ...ts.configs.disableTypeChecked,
  },
  {
    ignores: [
      '.svelte-kit/',
      'build/',
      'node_modules/',
      'dist/',
      'static/',
      'playwright-report/',
      'test-results/',
      '.histoire/',
      // CSS is not linted by eslint; stylelint covers it.
      '**/*.css',
    ],
  },
];
