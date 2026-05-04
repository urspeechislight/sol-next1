<!--
  Scope sidebar for the search route — facets for sect / canonical /
  century. Sticky on desktop. Pure presentational; the active counts are
  passed in.
-->
<script lang="ts">
  interface Counts {
    total: number;
    primary: number;
    sunni: number;
    imami: number;
  }
  interface Props {
    counts: Counts;
  }
  let { counts }: Props = $props();
</script>

<aside class="search__scope">
  <div class="scope">
    <div class="scope__head">Scope</div>
    <ul class="scope__list">
      <li><span>All books</span><span>{counts.total}</span></li>
      <li><span>Primary sources</span><span>{counts.primary}</span></li>
      <li><span>Imami</span><span>{counts.imami}</span></li>
      <li><span>Sunni</span><span>{counts.sunni}</span></li>
    </ul>
    <div class="scope__head scope__head--sub">Century (AH)</div>
    <ul class="scope__list">
      <li><span>1–3</span><span>8</span></li>
      <li><span>4–7</span><span>21</span></li>
      <li><span>8–12</span><span>14</span></li>
      <li><span>13+</span><span>6</span></li>
    </ul>
  </div>
</aside>

<style>
  .scope {
    position: sticky;
    top: 88px;
    background: var(--color-bg-1);
    border: 1px solid var(--color-border-1);
    border-radius: var(--radius-md);
    padding: 18px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .scope__head {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-accent);
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .scope__head--sub {
    border-top: 1px solid var(--color-border-1);
    padding-top: 12px;
    margin-top: 4px;
  }
  .scope__list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .scope__list li {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding: 6px 8px;
    border-radius: var(--radius-sm);
    font-family: var(--font-display);
    font-style: italic;
    font-size: var(--text-sm);
    color: var(--color-fg-2);
  }
  .scope__list li:hover {
    background: var(--color-bg-2);
    color: var(--color-fg-1);
  }
  .scope__list li > span:last-child {
    font-family: var(--font-mono);
    font-size: 10px;
    font-style: normal;
    color: var(--color-accent);
    letter-spacing: 0.12em;
  }
</style>
