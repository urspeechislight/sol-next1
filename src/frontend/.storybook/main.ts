import type { StorybookConfig } from '@storybook/sveltekit';

const config: StorybookConfig = {
  stories: ['../lib/**/*.mdx', '../lib/**/*.stories.@(js|ts|svelte)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-svelte-csf',
    '@storybook/addon-themes',
  ],
  framework: {
    name: '@storybook/sveltekit',
    options: {},
  },
  docs: { autodocs: 'tag' },
  typescript: {
    check: false,
  },
};

export default config;
