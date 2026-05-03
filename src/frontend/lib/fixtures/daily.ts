/**
 * Curated "today" picks — Verse of the Day with tafsir excerpts, Hadith of
 * the Day with isnād + grade, Book of the Day with editorial note, plus
 * a rotation list for the home carousel.
 *
 * In production these will rotate from a content calendar served by the
 * backend; here they are static but realistic.
 */

import type { DailyContent } from './types.js';

export const DAILY: DailyContent = {
  date: {
    hijri: '15 Jumādā al-Ūlā 1446',
    hijriShort: '15 / V / 1446',
    gregorian: '17 November 2024',
  },

  verse: {
    surah: 'al-Mulk',
    surahAr: 'الملك',
    surahN: 67,
    ayahN: 2,
    ayahAr:
      'الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا ۚ وَهُوَ الْعَزِيزُ الْغَفُورُ',
    ayahEn:
      'He who created death and life to test which of you is best in deed. And He is the Mighty, the Forgiving.',
    tafsirs: [
      {
        book: 'al-Mizan fi Tafsir al-Qurʾan',
        bookAr: 'الميزان في تفسير القرآن',
        author: 'al-Tabatabaʾi',
        urn: 'MizanQM',
        excerptEn:
          '"Best in deed" is not measured by abundance but by sincerity and conformity to what is right. Death is mentioned before life because the test demands awareness of finitude before living rightly within it.',
        excerptAr:
          '«أحسن عملا» لا يقاس بالكثرة بل بالإخلاص والانطباق على الحق؛ وقُدّم ذكر الموت لأن الاختبار يستدعي الوعي بالفناء قبل العيش في حدوده.',
      },
      {
        book: 'Jamiʿ al-Bayan',
        bookAr: 'جامع البيان',
        author: 'al-Tabari',
        urn: 'TafsTab',
        excerptEn:
          'The created order, its mortality and its quickening, is itself the apparatus of the trial. The verse closes on al-ʿAzīz al-Ghafūr to anchor accountability between power and pardon.',
        excerptAr:
          'الخَلق بفنائه وحياته هو ذاته آلة الاختبار، وقد ختمت الآية بـ«العزيز الغفور» لتثبت المحاسبة بين القدرة والمغفرة.',
      },
    ],
  },

  hadith: {
    matnAr:
      'مَنْ سَلَكَ طَرِيقًا يَطْلُبُ فِيهِ عِلْمًا سَلَكَ اللَّهُ بِهِ طَرِيقًا إِلَى الْجَنَّةِ، وَإِنَّ الْمَلَائِكَةَ لَتَضَعُ أَجْنِحَتَهَا لِطَالِبِ الْعِلْمِ رِضًا بِمَا يَصْنَعُ.',
    matnEn:
      'Whoever travels a path seeking knowledge upon it, God makes for him a path to Paradise; and the angels lower their wings for the seeker of knowledge, in approval of what he does.',
    isnadAr: 'عَنْ أَبِي الدَّرْدَاءِ، عَنِ النَّبِيِّ ﷺ',
    source: { book: 'Sunan Abi Dawud', bookAr: 'سنن أبي داود', n: 3641, urn: null, sect: 'sunni' },
    parallels: [
      { book: 'al-Kafi', bookAr: 'الكافي', n: '1/34/h.1', sect: 'imami', urn: 'KafSlm32' },
      { book: 'Sunan al-Tirmidhi', bookAr: 'سنن الترمذي', n: 2682, urn: null, sect: 'sunni' },
    ],
    grade: 'sahih',
    gradeLabel: 'Ṣaḥīḥ',
    note: 'A foundational ḥadīth on the merit of seeking knowledge, transmitted with multiple chains across Sunni and Imami collections.',
  },

  book: {
    urn: 'KafSlm32',
    rationale:
      'The earliest of the Four Books, read today for its opening Kitāb al-ʿAql wa-l-Jahl, the intellect as the first of God’s creations.',
    openTo: { page: 109, chapterEn: 'Kitāb al-Tawḥīd' },
  },

  rotation: [
    'MizanQM',
    'KafSlm32',
    'BukhJam2',
    'WasShia',
    'TafsTab',
    'FathBari',
    'OXlyzwsl',
    'TaqTah52',
  ],
};
