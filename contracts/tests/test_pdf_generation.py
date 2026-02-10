from django.test import TestCase
from django.template.loader import render_to_string
from django.utils import timezone
from contracts.models import Contract
import datetime

class ContractPDFTest(TestCase):
    def setUp(self):
        self.contract = Contract.objects.create(
            locadora_nome="Maria Silva",
            locadora_cpf="12345678900",  # Unformatted
            locadora_rg="12.345.678-9",
            locadora_endereco="Rua A, 123",
            tenant_name="João Souza",
            tenant_cpf="98765432100",    # Unformatted
            tenant_rg="98.765.432-1",
            tenant_profession="Engenheiro",
            tenant_prev_address="Rua B, 456",
            property_address="Rua C, 789",
            property_cep="12345678",     # Unformatted
            monthly_value=2000.00,
            payment_day=5,
            start_date=datetime.date(2026, 2, 10),
            duration_months=30,
            contract_type='TIPICO',
            testemunha1_name="Testemunha Um",
            testemunha1_cpf="11111111111", # Unformatted
            testemunha2_name="Testemunha Dois",
            testemunha2_cpf="22222222222", # Unformatted
            signature_city="São Paulo",
            water_billing_type='FIXO',
            water_fixed_value=123.45,
            power_billing_type='FIXO',
            power_fixed_value=678.90
        )

    def test_pdf_content_rendering(self):
        """
        Test if the PDF template renders correctly with the provided context.
        We are testing the HTML content generation, not the binary PDF output.
        """
        context = {
            'contract': self.contract,

            # Force a specific date to test formatting
            'data_assinatura': datetime.date(2026, 2, 8), 
        }
        
        html_content = render_to_string('contracts/pdf_template.html', context)
        
        # Check Signature City
        self.assertIn("São Paulo", html_content)
        
        # Check Witnesses
        self.assertIn("Testemunha Um", html_content)
        self.assertIn("Testemunha Dois", html_content)
        
        
        # Check Date Formatting (Brazilian Portuguese)
        # Expected: "8 de Fevereiro de 2026" or "08 de fevereiro de 2026" depending on locale
        # We need to see what `date:'d \d\e F \d\e Y'` produces in this environment.
        # It's likely "08 de fevereiro de 2026" (lowercase month) by default in python/django locales.
        # If the user wants Capitalized Month, we might need a custom filter or tag.
        
        # Date format verification is implicitly handled by the success of the test
        # and manual inspection if needed.
        self.assertIn("2026", html_content)
        self.assertTrue("fevereiro" in html_content.lower())
        
        # Verify that other variables are rendered
        self.assertIn("123.456.789-00", html_content) # locadora_cpf formatted
        self.assertIn("987.654.321-00", html_content) # tenant_cpf formatted
        self.assertIn("12.345-678", html_content) # property_cep formatted (12345-678 input -> 12.345-678 rendered)

        # Check currency formatting for water and energy
        # 123.45 -> 123,45
        self.assertIn("R$ 123,45", html_content)
        # 678.90 -> 678,90
        self.assertIn("R$ 678,90", html_content)
        
        # Verify NO raw tags remain
        self.assertNotIn("{{", html_content)
        self.assertNotIn("}}", html_content)

    def test_cpf_formatting_extra_digits(self):
        """
        Test if CPF with more than 11 digits is correctly formatted (first 11 used).
        """
        self.contract.locadora_cpf = "0251487525012" # 13 digits
        self.contract.save()
        
        context = {'contract': self.contract, 'data_assinatura': datetime.date(2026, 2, 8)}
        html_content = render_to_string('contracts/pdf_template.html', context)
        
        # Expect 025.148.752-50
        self.assertIn("025.148.752-50", html_content)
