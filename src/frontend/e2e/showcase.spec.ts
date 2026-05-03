import { expect, test } from '@playwright/test';

test('should_render_showcase_page_when_visiting_root', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Foundation showcase' })).toBeVisible();
});

test('should_toggle_theme_when_button_clicked', async ({ page }) => {
  await page.goto('/');
  const initial = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  await page.getByRole('button', { name: 'Toggle theme' }).click();
  const updated = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  expect(updated).not.toBe(initial);
});
