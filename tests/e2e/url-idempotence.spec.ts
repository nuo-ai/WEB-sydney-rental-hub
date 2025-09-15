import { test, expect } from '@playwright/test';

test.describe('URL 幂等与仅写非空键（排序入口冒烟）', () => {
  test('重复选择相同排序不应改变 URL（避免无意义 replace 循环）', async ({ page }) => {
    // 进入首页
    await page.goto('/');

    // 打开排序下拉
    const sortBtn = page.locator('button.sort-btn');
    await expect(sortBtn).toBeVisible();
    await sortBtn.click();

    // 选择“按最小价格” => sort=price_asc
    const priceAsc = page.getByRole('menuitem', { name: '按最小价格' });
    await priceAsc.click();

    // 等待 URL 包含 sort=price_asc
    await expect(page).toHaveURL(/[\?&]sort=price_asc(\b|&|$)/);
    const firstSearch = new URL(page.url()).search;

    // 再次打开下拉并选择相同项
    await sortBtn.click();
    await priceAsc.click();

    // URL 应保持不变（幂等）
    const secondSearch = new URL(page.url()).search;
    expect(secondSearch).toBe(firstSearch);
  });

  test('切换不同排序仅写有效键，URL 稳定无空值', async ({ page }) => {
    await page.goto('/');

    // 选择“按最小价格”
    await page.locator('button.sort-btn').click();
    await page.getByRole('menuitem', { name: '按最小价格' }).click();
    await expect(page).toHaveURL(/[\?&]sort=price_asc(\b|&|$)/);

    // 切换为“按空出时间” => sort=available_date_asc
    await page.locator('button.sort-btn').click();
    await page.getByRole('menuitem', { name: '按空出时间' }).click();

    await expect(page).toHaveURL(/[\?&]sort=available_date_asc(\b|&|$)/);

    // 断言：URL 中不存在空键（例如 ?minPrice=&xxx=）
    const url = new URL(page.url());
    const entries = Array.from(url.searchParams.entries());
    for (const [k, v] of entries) {
      expect(k.trim()).not.toBe('');
      expect(v.trim()).not.toBe('');
    }
  });
});
