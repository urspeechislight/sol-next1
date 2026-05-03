import { browser } from '$app/environment';
import { writable } from 'svelte/store';

export type Theme = 'dark' | 'light';

const STORAGE_KEY = 'theme';

function readInitial(): Theme {
  if (!browser) return 'dark';
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'dark' || stored === 'light') return stored;
  return matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

function applyTheme(theme: Theme): void {
  if (!browser) return;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(STORAGE_KEY, theme);
}

const internal = writable<Theme>(readInitial());

export const theme = {
  subscribe: internal.subscribe,
  set(value: Theme): void {
    internal.set(value);
    applyTheme(value);
  },
  toggle(): void {
    internal.update((t) => {
      const next: Theme = t === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      return next;
    });
  },
};
