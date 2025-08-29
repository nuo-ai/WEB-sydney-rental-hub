const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Mobile Filter Functionality Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set mobile viewport for iPhone 6/7/8
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Navigate to the website
    await page.goto('http://localhost:5173/');
    
    // Wait for the page to load completely
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000); // Additional wait for Vue components to mount
  });

  test('Mobile Filter Buttons - Comprehensive Test', async ({ page }) => {
    console.log('Starting comprehensive mobile filter test...');

    // Take initial screenshot
    await page.screenshot({ 
      path: 'mobile-initial-view.png',
      fullPage: true 
    });
    console.log('✅ Initial mobile view screenshot taken');

    // Check for console errors
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Test data structure to track results
    const testResults = {
      filterButton: { visible: false, clickable: false, opens: false },
      areaButton: { visible: false, clickable: false, opens: false },
      bedroomsButton: { visible: false, clickable: false, opens: false },
      priceButton: { visible: false, clickable: false, opens: false },
      availabilityButton: { visible: false, clickable: false, opens: false }
    };

    console.log('Testing filter button visibility and presence...');

    // 1. Test main "筛选" (Filter) button
    console.log('--- Testing 筛选 (Filter) button ---');
    const filterButton = page.locator('text=筛选').first();
    testResults.filterButton.visible = await filterButton.isVisible().catch(() => false);
    
    if (testResults.filterButton.visible) {
      console.log('✅ 筛选 button is visible');
      testResults.filterButton.clickable = await filterButton.isEnabled().catch(() => false);
      
      if (testResults.filterButton.clickable) {
        console.log('✅ 筛选 button is clickable');
        
        // Click the filter button
        await filterButton.click();
        await page.waitForTimeout(1000);
        
        // Check if filter panel opens
        const filterPanel = page.locator('[class*="filter-panel"], [class*="FilterPanel"], .filter-drawer, .el-drawer');
        testResults.filterButton.opens = await filterPanel.isVisible().catch(() => false);
        
        if (testResults.filterButton.opens) {
          console.log('✅ Filter panel opens when 筛选 button is clicked');
          await page.screenshot({ 
            path: 'mobile-filter-panel-open.png',
            fullPage: true 
          });
        } else {
          console.log('❌ Filter panel does not open when 筛选 button is clicked');
        }
        
        // Close the panel if it opened
        const closeButton = page.locator('[class*="close"], .el-drawer__close-btn, [aria-label="Close"]');
        if (await closeButton.isVisible().catch(() => false)) {
          await closeButton.click();
          await page.waitForTimeout(500);
        } else {
          // Try clicking outside to close
          await page.click('body', { position: { x: 10, y: 100 } });
          await page.waitForTimeout(500);
        }
      } else {
        console.log('❌ 筛选 button is not clickable');
      }
    } else {
      console.log('❌ 筛选 button is not visible');
    }

    // 2. Test "区域" (Area) button
    console.log('--- Testing 区域 (Area) button ---');
    const areaButton = page.locator('text=区域').first();
    testResults.areaButton.visible = await areaButton.isVisible().catch(() => false);
    
    if (testResults.areaButton.visible) {
      console.log('✅ 区域 button is visible');
      testResults.areaButton.clickable = await areaButton.isEnabled().catch(() => false);
      
      if (testResults.areaButton.clickable) {
        console.log('✅ 区域 button is clickable');
        
        await areaButton.click();
        await page.waitForTimeout(1000);
        
        // Check for dropdown or expanded content
        const dropdown = page.locator('.el-select-dropdown, [class*="dropdown"], [class*="area-options"]');
        testResults.areaButton.opens = await dropdown.isVisible().catch(() => false);
        
        if (testResults.areaButton.opens) {
          console.log('✅ Area dropdown opens');
          await page.screenshot({ 
            path: 'mobile-area-dropdown.png',
            fullPage: true 
          });
        } else {
          console.log('❌ Area dropdown does not open');
          await page.screenshot({ 
            path: 'mobile-area-no-dropdown.png',
            fullPage: true 
          });
        }
        
        // Try to close dropdown
        await page.click('body', { position: { x: 10, y: 100 } });
        await page.waitForTimeout(500);
      } else {
        console.log('❌ 区域 button is not clickable');
      }
    } else {
      console.log('❌ 区域 button is not visible');
    }

    // 3. Test "卧室" (Bedrooms) button
    console.log('--- Testing 卧室 (Bedrooms) button ---');
    const bedroomsButton = page.locator('text=卧室').first();
    testResults.bedroomsButton.visible = await bedroomsButton.isVisible().catch(() => false);
    
    if (testResults.bedroomsButton.visible) {
      console.log('✅ 卧室 button is visible');
      testResults.bedroomsButton.clickable = await bedroomsButton.isEnabled().catch(() => false);
      
      if (testResults.bedroomsButton.clickable) {
        console.log('✅ 卧室 button is clickable');
        
        await bedroomsButton.click();
        await page.waitForTimeout(1000);
        
        const dropdown = page.locator('.el-select-dropdown, [class*="dropdown"], [class*="bedroom-options"]');
        testResults.bedroomsButton.opens = await dropdown.isVisible().catch(() => false);
        
        if (testResults.bedroomsButton.opens) {
          console.log('✅ Bedrooms dropdown opens');
          await page.screenshot({ 
            path: 'mobile-bedrooms-dropdown.png',
            fullPage: true 
          });
        } else {
          console.log('❌ Bedrooms dropdown does not open');
        }
        
        await page.click('body', { position: { x: 10, y: 100 } });
        await page.waitForTimeout(500);
      } else {
        console.log('❌ 卧室 button is not clickable');
      }
    } else {
      console.log('❌ 卧室 button is not visible');
    }

    // 4. Test "价格" (Price) button
    console.log('--- Testing 价格 (Price) button ---');
    const priceButton = page.locator('text=价格').first();
    testResults.priceButton.visible = await priceButton.isVisible().catch(() => false);
    
    if (testResults.priceButton.visible) {
      console.log('✅ 价格 button is visible');
      testResults.priceButton.clickable = await priceButton.isEnabled().catch(() => false);
      
      if (testResults.priceButton.clickable) {
        console.log('✅ 价格 button is clickable');
        
        await priceButton.click();
        await page.waitForTimeout(1000);
        
        const dropdown = page.locator('.el-select-dropdown, [class*="dropdown"], [class*="price-options"]');
        testResults.priceButton.opens = await dropdown.isVisible().catch(() => false);
        
        if (testResults.priceButton.opens) {
          console.log('✅ Price dropdown opens');
          await page.screenshot({ 
            path: 'mobile-price-dropdown.png',
            fullPage: true 
          });
        } else {
          console.log('❌ Price dropdown does not open');
        }
        
        await page.click('body', { position: { x: 10, y: 100 } });
        await page.waitForTimeout(500);
      } else {
        console.log('❌ 价格 button is not clickable');
      }
    } else {
      console.log('❌ 价格 button is not visible');
    }

    // 5. Test "空出时间" (Availability) button
    console.log('--- Testing 空出时间 (Availability) button ---');
    const availabilityButton = page.locator('text=空出时间').first();
    testResults.availabilityButton.visible = await availabilityButton.isVisible().catch(() => false);
    
    if (testResults.availabilityButton.visible) {
      console.log('✅ 空出时间 button is visible');
      testResults.availabilityButton.clickable = await availabilityButton.isEnabled().catch(() => false);
      
      if (testResults.availabilityButton.clickable) {
        console.log('✅ 空出时间 button is clickable');
        
        await availabilityButton.click();
        await page.waitForTimeout(1000);
        
        const dropdown = page.locator('.el-select-dropdown, [class*="dropdown"], [class*="availability-options"]');
        testResults.availabilityButton.opens = await dropdown.isVisible().catch(() => false);
        
        if (testResults.availabilityButton.opens) {
          console.log('✅ Availability dropdown opens');
          await page.screenshot({ 
            path: 'mobile-availability-dropdown.png',
            fullPage: true 
          });
        } else {
          console.log('❌ Availability dropdown does not open');
        }
        
        await page.click('body', { position: { x: 10, y: 100 } });
        await page.waitForTimeout(500);
      } else {
        console.log('❌ 空出时间 button is not clickable');
      }
    } else {
      console.log('❌ 空出时间 button is not visible');
    }

    // Test filter synchronization
    console.log('--- Testing Filter Synchronization ---');
    
    // Try to open main filter panel and check if quick filters sync
    if (testResults.filterButton.visible && testResults.filterButton.clickable) {
      await filterButton.click();
      await page.waitForTimeout(1000);
      
      // Look for filter options in the panel
      const filterOptions = page.locator('[class*="filter-option"], .el-checkbox, .el-radio, input[type="checkbox"]');
      const optionCount = await filterOptions.count();
      
      if (optionCount > 0) {
        console.log(`✅ Found ${optionCount} filter options in the main panel`);
        await page.screenshot({ 
          path: 'mobile-filter-options.png',
          fullPage: true 
        });
      } else {
        console.log('❌ No filter options found in the main panel');
      }
    }

    // Final screenshot showing any issues
    await page.screenshot({ 
      path: 'mobile-test-final.png',
      fullPage: true 
    });

    // Report console errors
    if (consoleErrors.length > 0) {
      console.log('❌ Console Errors Found:');
      consoleErrors.forEach((error, index) => {
        console.log(`  ${index + 1}. ${error}`);
      });
    } else {
      console.log('✅ No console errors detected');
    }

    // Summary report
    console.log('\n=== TEST RESULTS SUMMARY ===');
    console.log('筛选 (Filter) button:', 
      testResults.filterButton.visible ? '✅ Visible' : '❌ Not Visible',
      testResults.filterButton.clickable ? '✅ Clickable' : '❌ Not Clickable',
      testResults.filterButton.opens ? '✅ Opens Panel' : '❌ Panel Doesn\'t Open'
    );
    
    console.log('区域 (Area) button:', 
      testResults.areaButton.visible ? '✅ Visible' : '❌ Not Visible',
      testResults.areaButton.clickable ? '✅ Clickable' : '❌ Not Clickable',
      testResults.areaButton.opens ? '✅ Opens Dropdown' : '❌ Dropdown Doesn\'t Open'
    );
    
    console.log('卧室 (Bedrooms) button:', 
      testResults.bedroomsButton.visible ? '✅ Visible' : '❌ Not Visible',
      testResults.bedroomsButton.clickable ? '✅ Clickable' : '❌ Not Clickable',
      testResults.bedroomsButton.opens ? '✅ Opens Dropdown' : '❌ Dropdown Doesn\'t Open'
    );
    
    console.log('价格 (Price) button:', 
      testResults.priceButton.visible ? '✅ Visible' : '❌ Not Visible',
      testResults.priceButton.clickable ? '✅ Clickable' : '❌ Not Clickable',
      testResults.priceButton.opens ? '✅ Opens Dropdown' : '❌ Dropdown Doesn\'t Open'
    );
    
    console.log('空出时间 (Availability) button:', 
      testResults.availabilityButton.visible ? '✅ Visible' : '❌ Not Visible',
      testResults.availabilityButton.clickable ? '✅ Clickable' : '❌ Not Clickable',
      testResults.availabilityButton.opens ? '✅ Opens Dropdown' : '❌ Dropdown Doesn\'t Open'
    );

    console.log('\n📸 Screenshots saved:');
    console.log('- mobile-initial-view.png (Initial mobile view)');
    if (testResults.filterButton.opens) console.log('- mobile-filter-panel-open.png (Filter panel open)');
    if (testResults.areaButton.opens) console.log('- mobile-area-dropdown.png (Area dropdown)');
    if (!testResults.areaButton.opens && testResults.areaButton.visible) console.log('- mobile-area-no-dropdown.png (Area no dropdown)');
    if (testResults.bedroomsButton.opens) console.log('- mobile-bedrooms-dropdown.png (Bedrooms dropdown)');
    if (testResults.priceButton.opens) console.log('- mobile-price-dropdown.png (Price dropdown)');
    if (testResults.availabilityButton.opens) console.log('- mobile-availability-dropdown.png (Availability dropdown)');
    console.log('- mobile-test-final.png (Final state)');

    // Assertions for test validation
    expect(testResults.filterButton.visible || testResults.areaButton.visible).toBe(true);
  });

  test('Property Filtering Functionality', async ({ page }) => {
    console.log('Testing property filtering functionality...');

    // Wait for properties to load
    await page.waitForSelector('[class*="property"], .property-card', { timeout: 10000 });
    
    // Count initial properties
    const initialProperties = await page.locator('[class*="property"], .property-card').count();
    console.log(`Initial property count: ${initialProperties}`);

    // Test if any filters actually filter properties
    if (initialProperties > 0) {
      // Try to interact with a filter and see if property count changes
      const filterButton = page.locator('text=筛选').first();
      if (await filterButton.isVisible().catch(() => false)) {
        await filterButton.click();
        await page.waitForTimeout(1000);

        // Look for any filter controls and try to use them
        const checkboxes = page.locator('input[type="checkbox"], .el-checkbox');
        const checkboxCount = await checkboxes.count();
        
        if (checkboxCount > 0) {
          // Click the first checkbox
          await checkboxes.first().click();
          await page.waitForTimeout(2000);
          
          // Count properties after filter
          const filteredProperties = await page.locator('[class*="property"], .property-card').count();
          console.log(`Properties after filter: ${filteredProperties}`);
          
          if (filteredProperties !== initialProperties) {
            console.log('✅ Filtering appears to be working');
          } else {
            console.log('❌ Filtering may not be working - property count unchanged');
          }
        }
      }
    }

    await page.screenshot({ 
      path: 'mobile-property-filtering.png',
      fullPage: true 
    });
  });
});