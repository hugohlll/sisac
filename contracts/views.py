from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from weasyprint import HTML
import datetime

from .models import Contract
from .services.calculator import calculate_deposit_installments

from .forms import ContractForm

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    
    def get_success_url(self):
        return reverse_lazy('contract-pdf', kwargs={'pk': self.object.pk})

def generate_pdf(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    
    # Calculate deposit installments if applicable
    deposit_p1 = 0
    deposit_p2 = 0
    if contract.security_deposit_payment_type == 'PARCELADO':
        deposit_p1, deposit_p2 = calculate_deposit_installments(contract.monthly_value)

    context = {
        'contract': contract,
        'deposit_p1': deposit_p1,
        'deposit_p2': deposit_p2,
        'data_assinatura': contract.start_date,
    }
    
    html_string = render_to_string('contracts/pdf_template.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{contract.tenant_name}.pdf"'
    
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    
    return response
