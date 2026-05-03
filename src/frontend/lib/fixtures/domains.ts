/**
 * The seven knowledge domains and their categories. Mirrors the
 * information architecture from ADR-0006.
 *
 * Counts here are illustrative — once the corpus pipeline is live the
 * backend will return real counts and this file becomes a fallback.
 */

import type { Domain } from './types.js';

export const DOMAINS: Domain[] = [
  {
    id: 'hadith',
    label: 'Hadith',
    labelAr: 'الحديث',
    blurb: 'Foundational collections, transmission, and the science of narrators.',
    categories: [
      {
        slug: 'shia-hadith-fiqh',
        label: 'Shia Hadith, Fiqh',
        labelAr: 'الحديث الفقهي الشيعي',
        count: 12,
      },
      {
        slug: 'shia-hadith-general',
        label: 'Shia Hadith, General',
        labelAr: 'الحديث الشيعي العام',
        count: 28,
      },
      {
        slug: 'shia-hadith-narrators',
        label: 'Shia Hadith, Narrators',
        labelAr: 'رجال الحديث الشيعي',
        count: 24,
      },
      {
        slug: 'sunni-hadith-fiqh',
        label: 'Sunni Hadith, Fiqh',
        labelAr: 'الحديث الفقهي السني',
        count: 19,
      },
      {
        slug: 'sunni-hadith-general',
        label: 'Sunni Hadith, General',
        labelAr: 'الحديث السني العام',
        count: 41,
      },
      {
        slug: 'sunni-hadith-narrators',
        label: 'Sunni Hadith, Narrators',
        labelAr: 'رجال الحديث السني',
        count: 33,
      },
      { slug: 'fiqh-terminology', label: 'Fiqh Terminology', labelAr: 'مصطلح الحديث', count: 9 },
    ],
  },
  {
    id: 'quran',
    label: 'Qurʾan Sciences',
    labelAr: 'علوم القرآن',
    blurb: 'Tafsir traditions and the disciplines surrounding the Qurʾanic text.',
    categories: [
      { slug: 'shia-tafsir', label: 'Shia Tafsir', labelAr: 'التفسير الشيعي', count: 21 },
      { slug: 'sunni-tafsir', label: 'Sunni Tafsir', labelAr: 'التفسير السني', count: 38 },
      { slug: 'quran-sciences', label: 'Qurʾanic Sciences', labelAr: 'علوم القرآن', count: 14 },
    ],
  },
  {
    id: 'fiqh',
    label: 'Fiqh',
    labelAr: 'الفقه',
    blurb: 'Jurisprudential schools, principles, and case law across centuries.',
    categories: [
      { slug: 'hanafi-fiqh', label: 'Hanafi Fiqh', labelAr: 'الفقه الحنفي', count: 17 },
      { slug: 'hanbali-fiqh', label: 'Hanbali Fiqh', labelAr: 'الفقه الحنبلي', count: 13 },
      { slug: 'maliki-fiqh', label: 'Maliki Fiqh', labelAr: 'الفقه المالكي', count: 15 },
      { slug: 'shafii-fiqh', label: 'Shafiʿi Fiqh', labelAr: 'الفقه الشافعي', count: 18 },
      { slug: 'zahiri-fiqh', label: 'Zahiri Fiqh', labelAr: 'الفقه الظاهري', count: 4 },
      { slug: 'zaidi-fiqh', label: 'Zaidi Fiqh', labelAr: 'الفقه الزيدي', count: 6 },
      {
        slug: 'shia-fiqh-8th-century',
        label: 'Shia Fiqh, 8th Century',
        labelAr: 'الفقه الشيعي ق٨',
        count: 11,
      },
      {
        slug: 'shia-fiqh-fatwas',
        label: 'Shia Fiqh, Fatwas',
        labelAr: 'الفتاوى الشيعية',
        count: 8,
      },
      {
        slug: 'shia-fiqh-pre-8th-century',
        label: 'Shia Fiqh, Pre-8th C.',
        labelAr: 'الفقه الشيعي قبل ق٨',
        count: 9,
      },
      {
        slug: 'shia-fiqh-principles',
        label: 'Shia Fiqh, Principles',
        labelAr: 'أصول الفقه الشيعي',
        count: 22,
      },
      {
        slug: 'sunni-fiqh-principles',
        label: 'Sunni Fiqh, Principles',
        labelAr: 'أصول الفقه السني',
        count: 26,
      },
      { slug: 'independent-fiqh', label: 'Independent Fiqh', labelAr: 'الفقه المستقل', count: 7 },
    ],
  },
  {
    id: 'theology',
    label: 'Theology & Sects',
    labelAr: 'الكلام والفرق',
    blurb: 'Kalam, doctrinal works, and the comparative study of schools.',
    categories: [
      { slug: 'shia-theology', label: 'Shia Theology', labelAr: 'الكلام الشيعي', count: 19 },
      { slug: 'sunni-theology', label: 'Sunni Theology', labelAr: 'الكلام السني', count: 23 },
      { slug: 'sects-schools', label: 'Sects & Schools', labelAr: 'الفرق والمذاهب', count: 11 },
    ],
  },
  {
    id: 'biography',
    label: 'Biography & History',
    labelAr: 'التراجم والتاريخ',
    blurb: 'Genealogies, Imamate biography, geography, and chronicles.',
    categories: [
      {
        slug: 'genealogy-biography',
        label: 'Genealogy & Biography',
        labelAr: 'الأنساب والتراجم',
        count: 31,
      },
      {
        slug: 'prophet-imams-biography',
        label: 'Prophet & Imams Biography',
        labelAr: 'سيرة النبي والأئمة',
        count: 27,
      },
      {
        slug: 'history-geography',
        label: 'History & Geography',
        labelAr: 'التاريخ والجغرافيا',
        count: 24,
      },
    ],
  },
  {
    id: 'sciences',
    label: 'Sciences',
    labelAr: 'العلوم',
    blurb: 'Arabic linguistics, logic, philosophy, medicine, and adjacent fields.',
    categories: [
      {
        slug: 'arabic-language-sciences',
        label: 'Arabic Language Sciences',
        labelAr: 'علوم اللغة العربية',
        count: 35,
      },
      {
        slug: 'logic-philosophy',
        label: 'Logic & Philosophy',
        labelAr: 'المنطق والفلسفة',
        count: 16,
      },
      { slug: 'medicine', label: 'Medicine', labelAr: 'الطب', count: 8 },
      { slug: 'other-sciences', label: 'Other Sciences', labelAr: 'علوم أخرى', count: 12 },
    ],
  },
  {
    id: 'devotional',
    label: 'Devotional & Other',
    labelAr: 'الأخلاق والأدعية وغيرها',
    blurb: 'Ethics, supplications, poetry, contemporary issues, manuscripts.',
    categories: [
      {
        slug: 'ethics-mysticism',
        label: 'Ethics & Mysticism',
        labelAr: 'الأخلاق والعرفان',
        count: 18,
      },
      {
        slug: 'supplications-visitations',
        label: 'Supplications & Visitations',
        labelAr: 'الأدعية والزيارات',
        count: 22,
      },
      {
        slug: 'poetry-collections',
        label: 'Poetry Collections',
        labelAr: 'الدواوين الشعرية',
        count: 14,
      },
      {
        slug: 'contemporary-islamic-issues',
        label: 'Contemporary Islamic Issues',
        labelAr: 'القضايا الإسلامية المعاصرة',
        count: 10,
      },
      {
        slug: 'journals-miscellaneous',
        label: 'Journals & Miscellaneous',
        labelAr: 'مجلات ومتفرقات',
        count: 7,
      },
      {
        slug: 'bibliographies-indexes',
        label: 'Bibliographies & Indexes',
        labelAr: 'الفهارس والببليوغرافيات',
        count: 9,
      },
      { slug: 'manuscripts', label: 'Manuscripts', labelAr: 'المخطوطات', count: 6 },
    ],
  },
];
