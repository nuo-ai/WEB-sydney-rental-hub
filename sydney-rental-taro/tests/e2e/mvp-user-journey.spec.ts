import { test, expect } from '@playwright/test';

test.describe('MVP User Journey', () => {
  const APP_URL = 'http://localhost:10086'; // Assuming local dev server runs here

  test('should allow a user to filter properties', async ({ page }) => {
    // Step 1: Visit homepage and assert initial properties are loaded
    await page.goto(APP_URL);
    await expect(page.locator('.property-card-class')).toHaveCount(0); // Placeholder for real card selector
    
    // Wait for skeleton to disappear and cards to appear
    await expect(page.locator('.property-card-skeleton-class')).toHaveCount(0); // Placeholder
    const initialCards = await page.locator('.property-card-class').count();
    expect(initialCards).toBeGreaterThan(0);

    // Step 2: Open the filter modal
    await page.getByRole('button', { name: '筛选' }).click();
    const filterModal = page.locator('.filter-modal-class'); // Placeholder
    await expect(filterModal).toBeVisible();

    // Step 3: Set filter conditions
    // These are placeholders and will need actual selectors from the implemented FilterModal
    await page.locator('#university-selector').selectOption({ label: 'UNSW' });
    await page.locator('#price-slider-min').fill('500');
    await page.locator('#price-slider-max').fill('1000');

    // Step 4: Apply filters and validate results
    await page.getByRole('button', { name: '查看房源' }).click();
    await expect(filterModal).toBeHidden();

    // Wait for new properties to load
    await expect(page.locator('.property-card-skeleton-class')).toHaveCount(0);
    
    // Assert that the property list has been updated
    const filteredCards = await page.locator('.property-card-class').count();
    expect(filteredCards).not.toBe(initialCards); // A simple check

    // A more robust check would be to inspect the content of the cards
    for (const card of await page.locator('.property-card-class').all()) {
      const priceText = await card.locator('.price-class').innerText(); // Placeholder
      const price = parseInt(priceText.replace(/[^0-9]/g, ''), 10);
      expect(price).toBeGreaterThanOrEqual(500);
      expect(price).toBeLessThanOrEqual(1000);
    }
  });
});
