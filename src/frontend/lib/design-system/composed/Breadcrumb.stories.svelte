<script module lang="ts">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Breadcrumb from './Breadcrumb.svelte';

  const { Story } = defineMeta({
    title: 'Composed/Breadcrumb',
    component: Breadcrumb,
    tags: ['autodocs'],
  });
</script>

<Story name="Three crumbs">
  <Breadcrumb
    items={[
      { label: 'Library', href: '/library' },
      { label: 'Hadith', href: '/library/hadith' },
      { label: 'Imami collections' },
    ]}
  />
</Story>

<Story name="Single crumb (current page only)">
  <Breadcrumb items={[{ label: 'Home' }]} />
</Story>

<Story name="Deep trail">
  <Breadcrumb
    items={[
      { label: 'Library', href: '/library' },
      { label: 'Hadith', href: '/library/hadith' },
      { label: 'al-Kāfī', href: '/book/al-kafi' },
      { label: 'Kitāb al-Tawḥīd', href: '/book/al-kafi/tawhid' },
      { label: 'Page 109' },
    ]}
  />
</Story>
