/* eslint-env node */
/* eslint-disable no-undef */
const { chromium } = require('playwright');

async function inspectImageViewer() {
  const browser = await chromium.launch({ headless: false }); // Set to false to see the browser
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  const page = await context.newPage();

  try {
    console.log('Navigating to property detail page...');

    // Navigate to the property detail page
    await page.goto('http://localhost:5173/properties/1');

    // Wait for the page to load
    await page.waitForTimeout(2000);

    // Find the main property image and click it to open the lightbox
    console.log('Looking for property images...');

    // Try different selectors for the main image
    const imageSelectors = [
      'img[src*="domain.com.au"]', // Domain images
      '.property-image img',
      '.main-image img',
      'img:first-of-type',
      '.el-image img'
    ];

    let imageFound = false;
    for (const selector of imageSelectors) {
      try {
        await page.waitForSelector(selector, { timeout: 3000 });
        console.log(`Found image with selector: ${selector}`);
        await page.click(selector);
        imageFound = true;
        break;
      } catch {
        console.log(`No image found with selector: ${selector}`);
      }
    }

    if (!imageFound) {
      console.log('No clickable image found. Looking for all images on page...');
      const allImages = await page.$$eval('img', imgs =>
        imgs.map(img => ({
          src: img.src,
          alt: img.alt,
          className: img.className,
          parentClass: img.parentElement?.className
        }))
      );
      console.log('All images on page:', allImages);

      // Try clicking the first image
      if (allImages.length > 0) {
        await page.click('img');
        imageFound = true;
      }
    }

    if (imageFound) {
      // Wait for the lightbox/image viewer to appear
      console.log('Waiting for image viewer to open...');
      await page.waitForTimeout(1000);

      // Look for various Element Plus image viewer selectors
      const viewerSelectors = [
        '.el-image-viewer',
        '.el-image-viewer__wrapper',
        '.el-image-viewer__mask',
        '.el-overlay',
        '.el-popper',
        '[class*="image-viewer"]',
        '[class*="lightbox"]',
        '[class*="overlay"]'
      ];

      console.log('\n=== DOM STRUCTURE ANALYSIS ===');

      for (const selector of viewerSelectors) {
        try {
          const elements = await page.$$(selector);
          if (elements.length > 0) {
            console.log(`\nFound ${elements.length} element(s) with selector: ${selector}`);

            for (let i = 0; i < elements.length; i++) {
              const element = elements[i];

              // Get element details
              const details = await element.evaluate(el => ({
                tagName: el.tagName,
                className: el.className,
                id: el.id,
                style: el.getAttribute('style'),
                computedStyle: {
                  display: window.getComputedStyle(el).display,
                  position: window.getComputedStyle(el).position,
                  zIndex: window.getComputedStyle(el).zIndex,
                  backgroundColor: window.getComputedStyle(el).backgroundColor,
                  background: window.getComputedStyle(el).background
                },
                innerHTML: el.innerHTML.length > 200 ?
                  el.innerHTML.substring(0, 200) + '...' :
                  el.innerHTML
              }));

              console.log(`Element ${i + 1}:`, JSON.stringify(details, null, 2));
            }
          }
        } catch {
          // Selector not found, continue
        }
      }

      // Get the complete DOM structure of the body to see what's actually there
      console.log('\n=== COMPLETE DOM STRUCTURE (body children) ===');
      const bodyChildren = await page.evaluate(() => {
        const body = document.body;
        const children = Array.from(body.children);

        return children.map(child => ({
          tagName: child.tagName,
          className: child.className,
          id: child.id,
          style: child.getAttribute('style'),
          hasImageViewerClass: child.className.includes('image') ||
                               child.className.includes('viewer') ||
                               child.className.includes('overlay') ||
                               child.className.includes('lightbox')
        }));
      });

      console.log('Body children:', JSON.stringify(bodyChildren, null, 2));

      // Check for teleported elements (Element Plus often teleports modals to body)
      console.log('\n=== CHECKING FOR TELEPORTED ELEMENTS ===');
      const teleportedElements = await page.evaluate(() => {
        const allElements = document.querySelectorAll('*');
        const relevantElements = [];

        allElements.forEach(el => {
          const className = el.className;
          if (typeof className === 'string' &&
              (className.includes('el-') &&
               (className.includes('image') ||
                className.includes('viewer') ||
                className.includes('overlay') ||
                className.includes('popper')))) {
            relevantElements.push({
              tagName: el.tagName,
              className: el.className,
              id: el.id,
              style: el.getAttribute('style'),
              parent: el.parentElement?.tagName,
              parentClass: el.parentElement?.className
            });
          }
        });

        return relevantElements;
      });

      console.log('Relevant teleported elements:', JSON.stringify(teleportedElements, null, 2));

      // Take a screenshot for visual reference
      await page.screenshot({
        path: 'C:\\Users\\nuoai\\Desktop\\WEB-sydney-rental-hub\\apps\\web\\image-viewer-screenshot.png',
        fullPage: true
      });
      console.log('\nScreenshot saved as image-viewer-screenshot.png');

      // Wait a bit to keep the viewer open for inspection
      console.log('\nKeeping browser open for 10 seconds for manual inspection...');
      await page.waitForTimeout(10000);

    } else {
      console.log('Could not find or click any image to open the viewer.');
    }

  } catch (error) {
    console.error('Error during inspection:', error);
  } finally {
    await browser.close();
  }
}

// Run the inspection
inspectImageViewer().catch(console.error);
