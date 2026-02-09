const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:8000';

(async () => {
    console.log(`Testing ${TARGET_URL}...`);
    const browser = await chromium.launch({ headless: true }); // Use headless: true for this environment unless debugging
    const page = await browser.newPage();

    try {
        await page.goto(TARGET_URL);
        const title = await page.title();
        console.log('Page loaded successfully.');
        console.log('Page Title:', title);

        if (!title) {
            console.error('ERROR: Page title is empty!');
            process.exit(1);
        }

        // Take a screenshot for verification
        await page.screenshot({ path: '/tmp/sanity_check.png', fullPage: true });
        console.log('📸 Screenshot saved to /tmp/sanity_check.png');

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
