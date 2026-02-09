const { chromium } = require('playwright');

const BASE_URL = process.env.BASE_URL || 'http://localhost:8000';

(async () => {
    console.log(`Testing Contract Creation at ${BASE_URL}...`);
    const browser = await chromium.launch({ headless: true });
    // Increase timeout for form filling and submission
    const context = await browser.newContext();
    const page = await context.newPage();
    page.setDefaultTimeout(30000);

    try {
        await page.goto(BASE_URL);
        console.log('Page loaded.');

        // Fill Locadora Data
        await page.fill('input[name="locadora_nome"]', 'Maria Silva');
        await page.fill('input[name="locadora_cpf"]', '12345678900');
        await page.fill('input[name="locadora_rg"]', '123456789');
        await page.fill('input[name="locadora_endereco"]', 'Rua da Locadora, 100');

        // Fill Tenant Data
        await page.fill('input[name="tenant_name"]', 'João Souza');
        await page.fill('input[name="tenant_cpf"]', '98765432100');
        await page.fill('input[name="tenant_rg"]', '987654321');
        await page.fill('input[name="tenant_profession"]', 'Desenvolvedor');
        await page.fill('textarea[name="tenant_prev_address"]', 'Rua Anterior, 50');

        // Fill Property Data
        await page.fill('textarea[name="property_address"]', 'Rua do Imóvel, 200');
        await page.fill('input[name="property_cep"]', '12345678');

        // Fill Financial Data
        await page.fill('input[name="monthly_value"]', '2500.00');
        await page.fill('input[name="payment_day"]', '10');

        // Handle date input (text vs date type)
        const dateInputType = await page.getAttribute('input[name="start_date"]', 'type');
        if (dateInputType === 'date') {
            await page.fill('input[name="start_date"]', '2026-03-01');
        } else {
            await page.fill('input[name="start_date"]', '01/03/2026');
        }

        await page.fill('input[name="duration_months"]', '30');
        await page.selectOption('select[name="contract_type"]', 'TIPICO');

        // Fill Guarantee
        await page.fill('input[name="security_deposit_months"]', '3');
        await page.selectOption('select[name="security_deposit_payment_type"]', 'VISTA');

        // Fill Extra Charges
        await page.fill('input[name="maintenance_fee"]', '150.00');
        await page.selectOption('select[name="water_billing_type"]', 'INCLUSO');
        await page.selectOption('select[name="power_billing_type"]', 'CONTA');

        // Fill Witnesses
        await page.fill('input[name="testemunha1_name"]', 'Testemunha Um');
        await page.fill('input[name="testemunha1_cpf"]', '11111111111');
        await page.fill('input[name="testemunha2_name"]', 'Testemunha Dois');
        await page.fill('input[name="testemunha2_cpf"]', '22222222222');

        // Fill Signature City
        await page.fill('input[name="signature_city"]', 'Rio de Janeiro');

        console.log('Submitting form...');

        const [response] = await Promise.all([
            // Wait for PDF response (status 200 and URL containing /pdf/)
            page.waitForResponse(resp => resp.url().includes('/pdf/') && resp.status() === 200, { timeout: 30000 }),
            // Click Submit
            (async () => {
                const submitBtn = page.locator('button[type="submit"]');
                if (await submitBtn.count() > 0) {
                    await submitBtn.click();
                } else {
                    await page.click('button:has-text("Salvar"), input[type="submit"]');
                }
            })()
        ]);

        console.log(`✅ PDF Generated! URL: ${response.url()}`);
        console.log('🎉 Contract Creation E2E test passed!');

    } catch (error) {
        console.error('❌ Test failed:', error.message);

        // Optional: Check for validation errors if failed
        try {
            const errors = await page.locator('.errorlist, .is-invalid, .invalid-feedback').allTextContents();
            if (errors.length > 0) {
                console.log('Validation Errors Found:', errors);
            }
        } catch (e) {
            // Ignore error checking failure
        }

        await page.screenshot({ path: '/tmp/create_contract_failure.png', fullPage: true });
        console.log('📸 Screenshot saved to /tmp/create_contract_failure.png');
        process.exit(1);
    } finally {
        await browser.close();
    }
})();
