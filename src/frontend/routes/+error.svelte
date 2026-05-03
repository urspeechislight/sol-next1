<script lang="ts">
  import { page } from '$app/state';
  import { Button, Card, PageHeader, Stack, Text } from '$lib/design-system';
</script>

<Stack gap={8} class="max-w-xl mx-auto py-16">
  <PageHeader
    title={`${page.status}`}
    subtitle={page.error?.message ?? 'Something went wrong.'}
  />
  <Card>
    <Stack gap={4}>
      <Text tone="secondary">
        The route <Text as="span" family="mono">{page.url.pathname}</Text> couldn't be served.
      </Text>
      <Stack direction="row" gap={2}>
        <Button intent="accent" onclick={() => history.back()}>Go back</Button>
        <Button intent="outline" onclick={() => location.assign('/')}>Home</Button>
      </Stack>
    </Stack>
  </Card>
</Stack>
