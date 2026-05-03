import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [tailwindcss(), sveltekit()],
  server: {
    fs: {
      allow: ['..'],
    },
  },
  test: {
    include: ['lib/**/*.{test,spec}.{ts,js}'],
    environment: 'jsdom',
    setupFiles: ['./vitest-setup.ts'],
    globals: true,
  },
});
