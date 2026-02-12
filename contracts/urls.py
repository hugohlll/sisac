from django.urls import path
from .views import (
    ContractCreateView, 
    ContractListView, 
    ContractUpdateView, 
    generate_pdf, 
    serve_document,
    PublicSolicitationCreateView, 
    SolicitationSuccessView
)

urlpatterns = [
    path('', ContractCreateView.as_view(), name='contract-create'),
    path('list/', ContractListView.as_view(), name='contract-list'),
    path('edit/<uuid:pk>/', ContractUpdateView.as_view(), name='contract-edit'),
    path('documento/<int:pk>/', serve_document, name='serve-document'),
    path('solicitar/', PublicSolicitationCreateView.as_view(), name='public-solicitation'),
    path('solicitacao-concluida/', SolicitationSuccessView.as_view(), name='solicitation-success'),
    path('contract/<uuid:pk>/pdf/', generate_pdf, name='contract-pdf'),
]
