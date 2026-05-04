<!--
  Home — Sol corpus reading instrument ("The Celestial Library").

  Composes the celestial library home page from the design prototype.
  A single CelestialSky lives behind every section so the page reads as
  one continuous manuscript-night sky from hero to colophon. All content
  sections sit above it.
-->
<script lang="ts">
  import CelestialSky from '$lib/components/home/CelestialSky.svelte';
  import Hero from '$lib/components/home/Hero.svelte';
  import DomainCabinet from '$lib/components/home/DomainCabinet.svelte';
  import DailyInstrument from '$lib/components/home/daily/DailyInstrument.svelte';
  import ReadingRoom from '$lib/components/home/ReadingRoom.svelte';
  import StatsMarquee from '$lib/components/home/StatsMarquee.svelte';
  import Colophon from '$lib/components/home/Colophon.svelte';
</script>

<CelestialSky />

<div class="home">
  <Hero />
  <DomainCabinet />
  <DailyInstrument />
  <ReadingRoom />
  <StatsMarquee />
  <Colophon />
</div>

<style>
  .home {
    position: relative;
    z-index: 1;
  }
</style>
