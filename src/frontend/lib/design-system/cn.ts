import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names with intelligent Tailwind conflict resolution.
 * Later classes win over earlier ones for the same utility group.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
