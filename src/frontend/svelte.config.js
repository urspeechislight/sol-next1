import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ precompress: true }),
    files: {
      routes: 'routes',
      lib: 'lib',
      params: 'params',
      assets: 'static',
      appTemplate: 'app.html',
      errorTemplate: 'error.html',
      hooks: {
        client: 'hooks.client',
        server: 'hooks.server',
        universal: 'hooks',
      },
      // serviceWorker uses SvelteKit's default; we don't ship one yet.
    },
    alias: {
      '$design-system': './lib/design-system',
      '$design-system/*': './lib/design-system/*',
    },
    typescript: {
      config: (config) => ({
        ...config,
        compilerOptions: {
          ...config.compilerOptions,
          strict: true,
          noUncheckedIndexedAccess: true,
          exactOptionalPropertyTypes: true,
        },
      }),
    },
  },
};

export default config;
