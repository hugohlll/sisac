from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('tenant_name', 'contract_type', 'start_date', 'monthly_value', 'created_at')
    search_fields = ('tenant_name', 'tenant_cpf', 'locadora_nome')
    list_filter = ('contract_type', 'payment_day')
