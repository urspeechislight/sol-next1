<!--
  Home — Sol corpus reading instrument.

  Composes the celestial library home page from the design prototype.
  Sections being landed in this PR:
    - Hero (editorial copy + salawat + search)
    - Domain Cabinet (seven drawers, click to expand)

  Sections deferred to follow-up PRs and currently NOT rendered:
    - Daily Instrument (live verse / isnad / folio panels)
    - Reading Room (featured-books carousel)
    - Stats Marquee
    - Colophon
    - Full-page starfield backdrop + corner cartouches
-->
<script lang="ts">
  import Hero from '$lib/components/home/Hero.svelte';
  import DomainCabinet from '$lib/components/home/DomainCabinet.svelte';
</script>

<Hero />
<DomainCabinet />
