import type { Handle, HandleServerError } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  return resolve(event);
};

export const handleError: HandleServerError = ({ error, event }) => {
  // TODO: wire into structured logger when observability is added.
  const message = error instanceof Error ? error.message : 'Unknown server error';
  return { message, route: event.route.id ?? 'unknown' };
};
