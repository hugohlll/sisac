const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    try {
        await page.goto('http://localhost:8000');
        // Django debug page structure
        const exception = await page.textContent('.exception_value');
        console.log('Exception:', exception);

        // Try to get the first frame local vars or location
        // The structure is complex, but let's try to get the summary
        const summary = await page.textContent('#summary');
        console.log('Summary:', summary);

    } catch (e) {
        console.log('Error during test:', e);
    }
    await browser.close();
})();
