from django.urls import path
from .views import ContractCreateView, generate_pdf

urlpatterns = [
    path('', ContractCreateView.as_view(), name='contract-create'),
    path('contract/<uuid:pk>/pdf/', generate_pdf, name='contract-pdf'),
]
