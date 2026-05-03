/**
 * Server-side HTTP client for talking to the backend API.
 *
 * - Reads `BACKEND_URL` from environment (defaults to localhost during dev).
 * - Uses `fetch` (Node 22+ has it native; SvelteKit's wrapped fetch is preferred
 *   when called from a +page.server.ts so request context propagates).
 * - Returns parsed JSON or throws a typed error.
 */

import { env } from '$env/dynamic/private';

export interface ApiError extends Error {
  status: number;
  body: unknown;
}

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
  fetchImpl?: typeof fetch;
}

const baseUrl = (): string => env.BACKEND_URL ?? 'http://localhost:8000';

export async function api<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, headers = {}, fetchImpl = fetch } = options;
  const url = `${baseUrl().replace(/\/$/, '')}${path}`;

  const response = await fetchImpl(url, {
    method,
    headers: {
      'content-type': 'application/json',
      accept: 'application/json',
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  const parsed: unknown = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const err = new Error(`Backend ${response.status} ${path}`) as ApiError;
    err.status = response.status;
    err.body = parsed;
    throw err;
  }

  return parsed as T;
}
