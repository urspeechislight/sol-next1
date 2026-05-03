/**
 * Public surface for prototype corpus fixtures.
 *
 * Routes import from `$lib/fixtures` while the backend is being wired.
 * When `lib/server/api-client.ts` exposes typed fetchers for these
 * resources, switch consumers from imports here to fetcher calls and
 * delete the fixtures.
 */

export { DOMAINS } from './domains.js';
export { BOOKS, findBook } from './books.js';
export { SAMPLE_TOC, SAMPLE_PAGE } from './reader.js';
export { DAILY } from './daily.js';

export type {
  Domain,
  Category,
  Book,
  HadithGrade,
  Narrator,
  CrossRef,
  Hadith,
  TocItem,
  BookPage,
  DailyContent,
  VerseOfDay,
  TafsirExcerpt,
  HadithOfDay,
  HadithSource,
  BookOfDay,
} from './types.js';
