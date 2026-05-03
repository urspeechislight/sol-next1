/**
 * Sample reader content — al-Kafi page 109, opening of Kitāb al-Tawḥīd.
 * Used by the reader route to demonstrate matn + isnād + cross-references.
 */

import type { BookPage, TocItem } from './types.js';

export const SAMPLE_TOC: TocItem[] = [
  { page: 1, title: 'مقدمة المؤلف', titleEn: 'Author’s Introduction' },
  { page: 11, title: 'كتاب العقل والجهل', titleEn: 'The Book of Intellect and Ignorance' },
  { page: 47, title: 'كتاب فضل العلم', titleEn: 'The Book of the Excellence of Knowledge' },
  { page: 109, title: 'كتاب التوحيد', titleEn: 'The Book of Divine Unity', active: true },
  { page: 184, title: 'كتاب الحجة', titleEn: 'The Book of Proof' },
  { page: 421, title: 'كتاب الإيمان والكفر', titleEn: 'The Book of Faith and Disbelief' },
  { page: 612, title: 'كتاب الدعاء', titleEn: 'The Book of Supplication' },
  { page: 738, title: 'كتاب فضل القرآن', titleEn: 'The Book of the Excellence of the Qurʾan' },
  { page: 791, title: 'كتاب العشرة', titleEn: 'The Book of Social Conduct' },
];

export const SAMPLE_PAGE: BookPage = {
  pageNumber: 109,
  totalPages: 2148,
  chapterTitle: 'كتاب التوحيد',
  chapterTitleEn: 'The Book of Divine Unity',
  sectionTitle: 'باب حدوث العالم وإثبات المُحدِث',
  sectionTitleEn: 'Chapter: The contingency of the world and the affirmation of its Originator',
  hadiths: [
    {
      n: 1,
      isnadAr:
        'عَلِيُّ بْنُ إِبْرَاهِيمَ، عَنْ أَبِيهِ، عَنِ الْعَبَّاسِ بْنِ عَمْرٍو الْفُقَيْمِيِّ، عَنْ هِشَامِ بْنِ الْحَكَمِ، فِي حَدِيثِ الزِّنْدِيقِ الَّذِي أَتَى أَبَا عَبْدِ اللَّهِ ﷷ',
      matnAr:
        'فَكَانَ مِنْ سُؤَالِهِ أَنْ قَالَ: كَيْفَ يَعْبُدُ اللَّهَ الْخَلْقُ وَلَمْ يَرَوْهُ؟ قَالَ ﷷ: «رَأَتْهُ الْقُلُوبُ بِنُورِ الْإِيمَانِ، وَأَثْبَتَتْهُ الْعُقُولُ بِيَقَظَتِهَا إِثْبَاتَ الْعَيَانِ، وَالْأَبْصَارُ لَا تُدْرِكُهُ، وَهُوَ يُدْرِكُ الْأَبْصَارَ، وَهُوَ اللَّطِيفُ الْخَبِيرُ».',
      matnEn:
        'Among his questions was: “How can creation worship God whom they have not seen?” He (peace be upon him) replied: “Hearts have seen Him by the light of faith, and intellects have affirmed Him with their wakefulness as one affirms what is witnessed; sight does not perceive Him, yet He perceives sight, He is the Subtle, the Aware.”',
      narrators: [
        {
          name: 'Hisham ibn al-Hakam',
          nameAr: 'هشام بن الحكم',
          role: 'Companion of al-Sadiq',
          grade: 'Trustworthy',
          d: 199,
        },
        {
          name: 'al-ʿAbbas ibn ʿAmr al-Fuqaymi',
          nameAr: 'العباس بن عمرو الفقيمي',
          role: 'Transmitter',
          grade: 'Reliable',
          d: 270,
        },
        {
          name: 'Ibrahim ibn Hashim',
          nameAr: 'إبراهيم بن هاشم',
          role: 'Father of ʿAli',
          grade: 'Trustworthy',
          d: 245,
        },
        {
          name: 'ʿAli ibn Ibrahim al-Qummi',
          nameAr: 'علي بن إبراهيم القمي',
          role: 'Compiler’s teacher',
          grade: 'Trustworthy',
          d: 307,
        },
      ],
      grade: 'sahih',
      crossRefs: [
        { book: 'al-Tawhid (Saduq)', bookAr: 'التوحيد للصدوق', chapter: 'Bab al-Ruʾya', page: 108 },
        { book: 'Bihar al-Anwar', bookAr: 'بحار الأنوار', chapter: 'Vol. 4', page: 44 },
      ],
    },
    {
      n: 2,
      isnadAr:
        'مُحَمَّدُ بْنُ يَحْيَى، عَنْ أَحْمَدَ بْنِ مُحَمَّدِ بْنِ عِيسَى، عَنِ ابْنِ أَبِي عُمَيْرٍ، عَنْ هِشَامِ بْنِ سَالِمٍ، عَنْ أَبِي عَبْدِ اللَّهِ ﷷ',
      matnAr:
        'قَالَ: «إِنَّ اللَّهَ تَبَارَكَ وَتَعَالَى خَلْوٌ مِنْ خَلْقِهِ، وَخَلْقُهُ خَلْوٌ مِنْهُ، وَكُلُّ مَا وَقَعَ عَلَيْهِ اسْمُ شَيْءٍ مَا خَلَا اللَّهَ فَهُوَ مَخْلُوقٌ، وَاللَّهُ خَالِقُ كُلِّ شَيْءٍ، تَبَارَكَ الَّذِي لَيْسَ كَمِثْلِهِ شَيْءٌ».',
      matnEn:
        'He (peace be upon him) said: “God, Blessed and Exalted, is distinct from His creation, and His creation is distinct from Him. Everything to which the name ‘thing’ applies, save God, is created; and God is the Creator of every thing. Blessed is He: there is nothing like Him.”',
      narrators: [
        {
          name: 'Hisham ibn Salim',
          nameAr: 'هشام بن سالم',
          role: 'Companion of al-Sadiq',
          grade: 'Trustworthy',
          d: 179,
        },
        {
          name: 'Ibn Abi ʿUmayr',
          nameAr: 'ابن أبي عمير',
          role: 'Major transmitter',
          grade: 'Eminent',
          d: 217,
        },
        {
          name: 'Ahmad ibn Muhammad ibn ʿIsa',
          nameAr: 'أحمد بن محمد بن عيسى',
          role: 'Qummi authority',
          grade: 'Trustworthy',
          d: 280,
        },
        {
          name: 'Muhammad ibn Yahya al-ʿAttar',
          nameAr: 'محمد بن يحيى العطار',
          role: 'Compiler’s teacher',
          grade: 'Trustworthy',
          d: 290,
        },
      ],
      grade: 'sahih',
      crossRefs: [
        {
          book: 'al-Tawhid (Saduq)',
          bookAr: 'التوحيد للصدوق',
          chapter: 'Bab al-Tawhid',
          page: 105,
        },
      ],
    },
  ],
};
