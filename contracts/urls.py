from django.urls import path
from .views import (
    ContractListView,
    ContractUpdateView, 
    generate_pdf, 
    serve_document,
    PublicSolicitationCreateView, 
    SolicitationSuccessView,
    InspectionPhotoUploadView,
    delete_inspection_photo,
)

urlpatterns = [
    path('', ContractListView.as_view(), name='contract-list'),
    path('edit/<uuid:pk>/', ContractUpdateView.as_view(), name='contract-edit'),
    path('documento/<int:pk>/', serve_document, name='serve-document'),
    path('solicitar/', PublicSolicitationCreateView.as_view(), name='public-solicitation'),
    path('solicitacao-concluida/', SolicitationSuccessView.as_view(), name='solicitation-success'),
    path('contract/<uuid:pk>/pdf/', generate_pdf, name='contract-pdf'),
    path('vistoria/<uuid:pk>/', InspectionPhotoUploadView.as_view(), name='inspection-photos'),
    path('vistoria/foto/<int:pk>/delete/', delete_inspection_photo, name='delete-inspection-photo'),
]
