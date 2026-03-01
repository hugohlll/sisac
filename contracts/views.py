import mimetypes
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, FileResponse
from django.views.generic import CreateView, DetailView, TemplateView, ListView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from generator.render import render_pdf
from .models import Contract, ContractDocument, InspectionPhoto

from .forms import ContractForm, TenantSolicitationForm, InspectionPhotoForm

class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    
    def get_success_url(self):
        return reverse_lazy('contract-pdf', kwargs={'pk': self.object.pk})

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'
    
    def get_queryset(self):
        # Ordena por status (PENDING primeiro) e depois por data de criação (mais novos primeiro)
        # Como 'PENDING' vem depois de 'APPROVED' alfabeticamente, podemos ordenar descrescente por status 
        # para pegar PENDING primeiro se usarmos ordem alfabética reversa: R > P > A. 
        # Mas PENDING é o foco. Vamos fazer simples: PENDING primeiro, depois created_at desc.
        return Contract.objects.order_by('-status', '-created_at')

class ContractUpdateView(LoginRequiredMixin, UpdateView):
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

@login_required
def generate_pdf(request, pk):
    import base64
    import mimetypes as mt

    contract = get_object_or_404(Contract, pk=pk)
    
    import urllib.request

    # Encode inspection photos as base64 data URIs for WeasyPrint
    inspection_photos_data = []
    for photo in contract.inspection_photos.all():
        data = None
        try:
            # Se for Cloudinary (produção), o path não existe ou open() lança NotImplementedError.
            # O mais seguro é pegar via URL se for arquivo remoto, ou path se local.
            url = photo.photo.url
            if url.startswith('http'):
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = response.read()
            else:
                photo.photo.open('rb')
                data = photo.photo.read()
                photo.photo.close()
            
            if not data:
                continue

            # Detect content type
            ext = photo.photo.name.rsplit('.', 1)[-1].lower()
            content_type = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png'}.get(ext, 'image/jpeg')
            
            b64 = base64.b64encode(data).decode('utf-8')
            data_uri = f'data:{content_type};base64,{b64}'
            
            inspection_photos_data.append({
                'data_uri': data_uri,
                'description': photo.description,
                'uploaded_at': photo.uploaded_at,
            })
        except Exception as e:
            print(f"Error loading photo {photo.id} for PDF: {e}")
            continue
    
    context = {
        'contract': contract,
        'data_assinatura': contract.start_date,
        'inspection_photos_data': inspection_photos_data,
    }
    
    filename = f'contrato_{contract.tenant_name}.pdf'
    return render_pdf('contracts/pdf_template.html', context, filename, request.build_absolute_uri())


@login_required
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


class InspectionPhotoUploadView(LoginRequiredMixin, View):
    """Public page for landlord to upload property inspection photos."""
    
    def get(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        form = InspectionPhotoForm()
        photos = contract.inspection_photos.all()
        return render(request, 'contracts/inspection_photo_upload.html', {
            'contract': contract,
            'form': form,
            'photos': photos,
        })
    
    def post(self, request, pk):
        contract = get_object_or_404(Contract, pk=pk)
        form = InspectionPhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            files = request.FILES.getlist('photos')
            for f in files:
                InspectionPhoto.objects.create(contract=contract, photo=f)
            return redirect(reverse('inspection-photos', kwargs={'pk': contract.pk}))
        
        photos = contract.inspection_photos.all()
        return render(request, 'contracts/inspection_photo_upload.html', {
            'contract': contract,
            'form': form,
            'photos': photos,
        })


@login_required
def delete_inspection_photo(request, pk):
    """Delete an inspection photo (POST only)."""
    photo = get_object_or_404(InspectionPhoto, pk=pk)
    contract_pk = photo.contract.pk
    if request.method == 'POST':
        photo.photo.delete(save=False)
        photo.delete()
    return redirect(reverse('inspection-photos', kwargs={'pk': contract_pk}))

