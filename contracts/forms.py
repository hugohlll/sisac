from django import forms
from .models import Contract
import re

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
    
    def clean_field_helper(self, field_name):
        data = self.cleaned_data.get(field_name)
        if data:
            # Remove non-digit characters (keep alphanumerics for RG if needed, but usually RG is just numbers/X)
            # For CPF and CEP, strictly digits or hyphen? 
            # Model expects max_length=9 for CEP. 21.235-650 is 10 chars. 21235-650 is 9.
            # Best is to strip everything except digits and maybe hyphen if it fits?
            # Let's strip completely to digits for CPF (11 chars) and CEP (8 chars).
            # But we need to check if we want to save formatted or unformatted.
            # SPEC didn't enforce storage format, but validation is failing on length.
            # So stripping is safest.
            return re.sub(r'\D', '', data) 
        return data

    def clean_property_cep(self):
        # User input: 21.235-650 (10 chars). Clean to 21235650 (8 chars)
        cep = self.clean_field_helper('property_cep')
        # Optional: format back to 21235-650 (9 chars) if we want to save formatted
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return cep

    def clean_locadora_cpf(self):
        return self.clean_field_helper('locadora_cpf')

    def clean_tenant_cpf(self):
        return self.clean_field_helper('tenant_cpf')
    
    def clean_testemunha1_cpf(self):
        return self.clean_field_helper('testemunha1_cpf')

    def clean_testemunha2_cpf(self):
        return self.clean_field_helper('testemunha2_cpf')
