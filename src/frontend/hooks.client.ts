import type { HandleClientError } from '@sveltejs/kit';

export const handleError: HandleClientError = ({ error, event }) => {
  const message = error instanceof Error ? error.message : 'Unknown client error';
  return { message, route: event.route.id ?? 'unknown' };
};
