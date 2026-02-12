from django.contrib import admin
from .models import Contract, ContractDocument

class ContractDocumentInline(admin.TabularInline):
    model = ContractDocument
    extra = 0
    readonly_fields = ('file', 'uploaded_at')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('tenant_name', 'contract_type', 'status', 'start_date', 'monthly_value', 'created_at')
    search_fields = ('tenant_name', 'tenant_cpf', 'locadora_nome')
    list_filter = ('contract_type', 'status', 'payment_day')
    inlines = [ContractDocumentInline]

@admin.register(ContractDocument)
class ContractDocumentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)

