const { chromium } = require('playwright');

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';

(async () => {
    console.log(`Testing Home Page at ${BASE_URL}...`);
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    try {
        await page.goto(BASE_URL);

        // 1. Check Title
        const title = await page.title();
        if (!title.includes('SAC')) {
            throw new Error(`Title mismatch. Expected 'SAC' in '${title}'`);
        }
        console.log('✅ Title check passed');

        // 2. Check Main Header
        const h1 = await page.textContent('h1');
        if (!h1.includes('SAC - Contratos')) {
            throw new Error(`H1 mismatch. Expected 'SAC - Contratos', found '${h1}'`);
        }
        console.log('✅ H1 check passed');

        // 3. Check Section Headers
        await page.waitForSelector('text=Emitir Novo Contrato');
        console.log('✅ "Emitir Novo Contrato" section found');

        await page.waitForSelector('text=Dados da Locadora');
        console.log('✅ "Dados da Locadora" section found');

        // 5. Check Footer
        await page.waitForSelector('text=Sistema de Automação de Contratos');
        console.log('✅ Footer check passed');

        console.log('🎉 Home Page tests passed!');

    } catch (error) {
        console.error('❌ Error:', error.message);
        await page.screenshot({ path: '/tmp/home_error.png', fullPage: true });
        console.log('📸 Error screenshot saved to /tmp/home_error.png');
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
