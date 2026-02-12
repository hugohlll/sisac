import mimetypes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.views.generic import CreateView, DetailView, TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from generator.render import render_pdf
from .models import Contract, ContractDocument

from .forms import ContractForm, TenantSolicitationForm

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    
    def get_success_url(self):
        return reverse_lazy('contract-pdf', kwargs={'pk': self.object.pk})

class ContractListView(ListView):
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'
    
    def get_queryset(self):
        # Ordena por status (PENDING primeiro) e depois por data de criação (mais novos primeiro)
        # Como 'PENDING' vem depois de 'APPROVED' alfabeticamente, podemos ordenar descrescente por status 
        # para pegar PENDING primeiro se usarmos ordem alfabética reversa: R > P > A. 
        # Mas PENDING é o foco. Vamos fazer simples: PENDING primeiro, depois created_at desc.
        return Contract.objects.order_by('-status', '-created_at')

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    
    def get_success_url(self):
        return reverse_lazy('contract-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'APPROVED'
        self.object.save()
        return super().form_valid(form)

class PublicSolicitationCreateView(CreateView):
    model = Contract
    form_class = TenantSolicitationForm
    template_name = 'contracts/public_solicitation_form.html'
    
    def form_valid(self, form):
        # 1. Salva o Contrato (Pai)
        self.object = form.save(commit=False)
        self.object.status = 'PENDING'
        self.object.save()
        
        # 2. Processa os Arquivos
        files = self.request.FILES.getlist('documents')
        for f in files:
            ContractDocument.objects.create(contract=self.object, file=f)
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('solicitation-success')

class SolicitationSuccessView(TemplateView):
    template_name = 'contracts/solicitation_success.html'

def generate_pdf(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    
    context = {
        'contract': contract,
        'data_assinatura': contract.start_date,
    }
    
    filename = f'contrato_{contract.tenant_name}.pdf'
    return render_pdf('contracts/pdf_template.html', context, filename, request.build_absolute_uri())


def serve_document(request, pk):
    """Serve a ContractDocument with the correct detected content type."""
    doc = get_object_or_404(ContractDocument, pk=pk)

    # Read first bytes to detect actual file type
    doc.file.open('rb')
    header = doc.file.read(16)
    doc.file.seek(0)

    # Detect content type from magic bytes
    if header[:4] == b'%PDF':
        content_type = 'application/pdf'
    elif header[:3] == b'\xff\xd8\xff':
        content_type = 'image/jpeg'
    elif header[:8] == b'\x89PNG\r\n\x1a\n':
        content_type = 'image/png'
    else:
        content_type, _ = mimetypes.guess_type(doc.file.name)
        content_type = content_type or 'application/octet-stream'

    response = FileResponse(doc.file, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{doc.file.name.split("/")[-1]}"'
    return response

