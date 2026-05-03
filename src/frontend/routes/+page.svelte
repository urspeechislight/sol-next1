<script lang="ts">
  import {
    Badge,
    Button,
    Card,
    HealthBadge,
    Input,
    MetricCard,
    PageHeader,
    Stack,
    Text,
  } from '$lib/design-system';
</script>

<PageHeader
  title="Foundation showcase"
  subtitle="Every element on this page is a design-system primitive. Edit tokens.css to change everything."
>
  {#snippet actions()}
    <Stack direction="row" gap={2}>
      <Button intent="ghost" size="sm">Docs</Button>
      <Button intent="accent" size="sm">Get started</Button>
    </Stack>
  {/snippet}
</PageHeader>

<Stack gap={8}>
  <section>
    <Text as="h2" size="xl" weight="semibold" family="display" class="mb-4">Metrics</Text>
    <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
      <MetricCard label="Manuscripts" value="142" trend="up" delta="+8 this month" />
      <MetricCard label="Pages parsed" value="38,210" trend="up" delta="+1.2K" />
      <MetricCard label="Open issues" value="7" trend="down" delta="-3" />
      <MetricCard label="Avg confidence" value="0.91" trend="flat" delta="0.00" />
    </div>
  </section>

  <section>
    <Text as="h2" size="xl" weight="semibold" family="display" class="mb-4">Buttons</Text>
    <Card>
      <Stack direction="row" gap={3} wrap>
        <Button>Accent (default)</Button>
        <Button intent="subtle">Subtle</Button>
        <Button intent="outline">Outline</Button>
        <Button intent="ghost">Ghost</Button>
        <Button intent="danger">Danger</Button>
        <Button size="sm">Small</Button>
        <Button size="lg">Large</Button>
        <Button disabled>Disabled</Button>
      </Stack>
    </Card>
  </section>

  <section>
    <Text as="h2" size="xl" weight="semibold" family="display" class="mb-4">Badges</Text>
    <Card>
      <Stack direction="row" gap={2} wrap>
        <Badge status="accent">accent</Badge>
        <Badge status="success">success</Badge>
        <Badge status="warning">warning</Badge>
        <Badge status="danger">danger</Badge>
        <Badge status="info">info</Badge>
        <Badge status="muted">muted</Badge>
        <Badge status="success" variant="outline">outline</Badge>
        <HealthBadge band="strong" score={94} />
        <HealthBadge band="at_risk" score={62} />
        <HealthBadge band="critical" score={31} />
      </Stack>
    </Card>
  </section>

  <section>
    <Text as="h2" size="xl" weight="semibold" family="display" class="mb-4">Inputs</Text>
    <Card>
      <Stack gap={3} class="max-w-md">
        <Input placeholder="Default" />
        <Input placeholder="Error state" state="error" />
        <Input placeholder="Success state" state="success" />
        <Input placeholder="Small" size="sm" />
        <Input placeholder="Large" size="lg" />
      </Stack>
    </Card>
  </section>

  <section>
    <Text as="h2" size="xl" weight="semibold" family="display" class="mb-4">Type scale</Text>
    <Card>
      <Stack gap={2}>
        <Text size="4xl" weight="semibold" family="display">Display 4xl</Text>
        <Text size="3xl" weight="semibold" family="display">Display 3xl</Text>
        <Text size="2xl" weight="medium">Heading 2xl</Text>
        <Text size="xl">Heading xl</Text>
        <Text size="lg" tone="secondary">Subheading lg secondary</Text>
        <Text>Body base</Text>
        <Text size="sm" tone="tertiary">Caption sm tertiary</Text>
        <Text family="mono" size="sm">monospace 14 / 0.875rem</Text>
      </Stack>
    </Card>
  </section>
</Stack>
