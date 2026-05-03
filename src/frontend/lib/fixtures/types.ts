/**
 * Type contracts for the corpus prototype fixtures.
 *
 * These types describe the shape of `lib/fixtures/*` — curated sample data
 * that drives the UI in lieu of a live backend. When the FastAPI
 * `backend/routers/books.py` etc. are wired and `lib/server/api-client.ts`
 * exposes typed fetchers, route components should switch from importing
 * fixtures to calling the api-client. The shapes here intentionally mirror
 * what those endpoints will eventually return.
 *
 * Color/badge decisions for `sect` and `canonical` live in `variants.ts` —
 * never re-derive them here.
 */

import type { Sect, CanonicalTier } from '../design-system/variants.js';

/** A top-level knowledge domain (Hadith, Qur'an Sciences, Fiqh, ...). */
export interface Domain {
  /** Stable slug used in URLs and navigation. */
  id: string;
  /** English label. */
  label: string;
  /** Arabic label. */
  labelAr: string;
  /** One-line editorial blurb. */
  blurb: string;
  /** Categories that roll up to this domain. */
  categories: Category[];
}

/** A category sits under a domain and groups related books. */
export interface Category {
  slug: string;
  label: string;
  labelAr: string;
  /** Number of books indexed in this category. */
  count: number;
}

/** A book entity — drives `BookCard` and detail views. */
export interface Book {
  /** Stable opaque identifier. */
  urn: string;
  titleAr: string;
  titleEn: string;
  author: string;
  authorAr: string;
  /** Author's death year in Hijri reckoning. */
  deathYearAh: number;
  /** Author's death year in Gregorian reckoning. */
  deathYearCe: number;
  pageCount: number;
  /** Slug of the parent category (matches `Category.slug`). */
  category: string;
  sect: Sect;
  /** Madhab where applicable; `null` for cross-school works. */
  madhab: string | null;
  canonical: CanonicalTier;
  /** Currently always 'Arabic' but typed for future expansion. */
  language: 'Arabic';
  blurb: string;
}

/** Hadith authentication grade — distinct from book canonical tier. */
export type HadithGrade = 'sahih' | 'hasan' | 'daif' | 'mawdu' | 'unknown';

/** A single narrator in an isnad chain. */
export interface Narrator {
  name: string;
  nameAr: string;
  /** Editorial role label, e.g. 'Companion of al-Sadiq'. */
  role: string;
  /** Reliability grade, e.g. 'Trustworthy'. */
  grade: string;
  /** Death year in AH. */
  d: number;
}

/** A cross-reference to the same hadith in another collection. */
export interface CrossRef {
  book: string;
  bookAr: string;
  chapter: string;
  page: number;
}

/** A single hadith record on a page. */
export interface Hadith {
  /** Sequence number within the page. */
  n: number;
  isnadAr: string;
  matnAr: string;
  matnEn: string;
  narrators: Narrator[];
  grade: HadithGrade;
  crossRefs: CrossRef[];
}

/** Table-of-contents entry for the reader. */
export interface TocItem {
  page: number;
  title: string;
  titleEn: string;
  active?: boolean;
}

/** One page of a book — the unit the reader displays. */
export interface BookPage {
  pageNumber: number;
  totalPages: number;
  chapterTitle: string;
  chapterTitleEn: string;
  sectionTitle: string;
  sectionTitleEn: string;
  hadiths: Hadith[];
}

/** Daily editorial content for the home page. */
export interface DailyContent {
  date: {
    hijri: string;
    hijriShort: string;
    gregorian: string;
  };
  verse: VerseOfDay;
  hadith: HadithOfDay;
  book: BookOfDay;
  /** URNs of books featured in the home rotation carousel, in order. */
  rotation: string[];
}

export interface VerseOfDay {
  surah: string;
  surahAr: string;
  surahN: number;
  ayahN: number;
  ayahAr: string;
  ayahEn: string;
  tafsirs: TafsirExcerpt[];
}

export interface TafsirExcerpt {
  book: string;
  bookAr: string;
  author: string;
  /** URN of the source book in `BOOKS`. */
  urn: string;
  excerptEn: string;
  excerptAr: string;
}

export interface HadithOfDay {
  matnAr: string;
  matnEn: string;
  isnadAr: string;
  source: HadithSource;
  parallels: HadithSource[];
  grade: HadithGrade;
  gradeLabel: string;
  note: string;
}

export interface HadithSource {
  book: string;
  bookAr: string;
  /** Hadith number or reference within the book. */
  n: number | string;
  /** URN if the parallel is in the indexed corpus, otherwise null. */
  urn: string | null;
  sect: Sect;
}

export interface BookOfDay {
  /** URN pointing into `BOOKS`. */
  urn: string;
  rationale: string;
  openTo: { page: number; chapterEn: string };
}
