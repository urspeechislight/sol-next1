<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import BookCard from './BookCard.svelte';

  const { Story } = defineMeta({
    title: 'Composed/BookCard',
    component: BookCard,
    tags: ['autodocs'],
    argTypes: {
      layout: { control: { type: 'select' }, options: ['row', 'card'] },
    },
  });

  const kafi = {
    urn: 'urn:sol:al-kafi',
    titleArabic: 'الكافي',
    titleLatin: 'al-Kāfī',
    author: 'Muḥammad ibn Yaʿqūb al-Kulaynī',
    authorAh: 329,
    pages: 2148,
    sect: 'imami' as const,
    canonical: 'primary' as const,
  };

  const bukhari = {
    urn: 'urn:sol:sahih-al-bukhari',
    titleArabic: 'صحيح البخاري',
    titleLatin: 'Ṣaḥīḥ al-Bukhārī',
    author: 'Muḥammad ibn Ismāʿīl al-Bukhārī',
    authorAh: 256,
    pages: 1814,
    sect: 'sunni' as const,
    canonical: 'primary' as const,
  };

  const fath = {
    urn: 'urn:sol:fath-al-bari',
    titleArabic: 'فتح الباري بشرح صحيح البخاري',
    titleLatin: 'Fatḥ al-Bārī',
    author: 'Ibn Ḥajar al-ʿAsqalānī',
    authorAh: 852,
    pages: 7800,
    sect: 'sunni' as const,
    canonical: 'commentary' as const,
  };

  const mizan = {
    urn: 'urn:sol:al-mizan',
    titleArabic: 'الميزان في تفسير القرآن',
    titleLatin: 'al-Mīzān fī Tafsīr al-Qurʾān',
    author: 'al-Ṭabāṭabāʾī',
    authorAh: 1402,
    pages: 5400,
    sect: 'imami' as const,
    canonical: 'commentary' as const,
  };
</script>

<Story name="Card layout">
  <div class="grid max-w-4xl grid-cols-2 gap-4">
    <BookCard book={kafi} layout="card" />
    <BookCard book={bukhari} layout="card" />
    <BookCard book={fath} layout="card" />
    <BookCard book={mizan} layout="card" />
  </div>
</Story>

<Story name="Row layout">
  <div class="flex max-w-4xl flex-col gap-3">
    <BookCard book={kafi} layout="row" />
    <BookCard book={bukhari} layout="row" />
    <BookCard book={fath} layout="row" />
    <BookCard book={mizan} layout="row" />
  </div>
</Story>

<Story name="Minimal book (no canonical, no pages)">
  <div class="grid max-w-4xl grid-cols-2 gap-4">
    <BookCard
      book={{
        urn: 'urn:sol:misc',
        titleArabic: 'كتاب مجهول',
        sect: 'unknown',
      }}
      layout="card"
    />
  </div>
</Story>
