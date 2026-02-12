from django.db import models
import uuid

class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendente de Análise'),
        ('APPROVED', 'Aprovado/Finalizado'),
        ('REJECTED', 'Rejeitado'),
    ]
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        verbose_name="Status"
    )
    
    # Dados da Locadora
    locadora_nome = models.CharField(max_length=255, verbose_name="Nome da Locadora", null=True, blank=True)
    locadora_cpf = models.CharField(max_length=14, verbose_name="CPF da Locadora", null=True, blank=True)
    locadora_rg = models.CharField(max_length=20, verbose_name="RG da Locadora", null=True, blank=True)
    locadora_endereco = models.CharField(max_length=255, verbose_name="Endereço da Locadora", null=True, blank=True)
    
    # Dados do Locatário
    tenant_name = models.CharField(max_length=255, verbose_name="Nome do Locatário")
    tenant_cpf = models.CharField(max_length=14, verbose_name="CPF do Locatário")
    tenant_rg = models.CharField(max_length=20, verbose_name="RG do Locatário")
    tenant_profession = models.CharField(max_length=100, verbose_name="Profissão do Locatário")
    tenant_prev_address = models.TextField(verbose_name="Endereço Anterior do Locatário")
    
    # Dados do Imóvel
    property_address = models.TextField(verbose_name="Endereço do Imóvel", null=True, blank=True)
    property_cep = models.CharField(max_length=9, verbose_name="CEP do Imóvel", null=True, blank=True)
    
    # Financeiro e Prazos
    monthly_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Mensal", null=True, blank=True)
    payment_day = models.PositiveIntegerField(default=10, verbose_name="Dia do Pagamento")
    start_date = models.DateField(verbose_name="Data de Início", null=True, blank=True)
    duration_months = models.PositiveIntegerField(default=30, verbose_name="Duração em Meses")
    
    CONTRACT_TYPE_CHOICES = [
        ('TIPICO', 'Típico (30 meses)'),
        ('ATIPICO', 'Atípico'),
    ]
    contract_type = models.CharField(
        max_length=10, 
        choices=CONTRACT_TYPE_CHOICES,
        verbose_name="Tipo de Contrato"
    )
    justification_atipico = models.TextField(null=True, blank=True, verbose_name="Justificativa (se Atípico)")
    
    # Garantia
    security_deposit_months = models.PositiveIntegerField(default=3, verbose_name="Meses de Caução")
    
    PAYMENT_TYPE_CHOICES = [
        ('VISTA', 'À Vista'),
    ]
    security_deposit_payment_type = models.CharField(
        max_length=20, 
        choices=PAYMENT_TYPE_CHOICES,
        default='VISTA',
        verbose_name="Forma de Pagamento da Caução"
    )
    
    # Encargos Extras
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Taxa de Manutenção")
    
    WATER_BILLING_CHOICES = [
        ('INCLUSO', 'Incluso no Aluguel'),
        ('FIXO', 'Valor Fixo'),
    ]
    water_billing_type = models.CharField(max_length=20, choices=WATER_BILLING_CHOICES, verbose_name="Cobrança de Água")
    water_fixed_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Fixo Água")
    
    POWER_BILLING_CHOICES = [
        ('INCLUSO', 'Incluso no Aluguel'),
        ('FIXO', 'Valor Fixo'),
        ('CONTA', 'Conta Individual'),
    ]
    power_billing_type = models.CharField(max_length=20, choices=POWER_BILLING_CHOICES, verbose_name="Cobrança de Energia")
    power_fixed_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Fixo Energia")
    
    testemunha1_name = models.CharField(max_length=255, verbose_name="Nome Testemunha 1", default="")
    testemunha1_cpf = models.CharField(max_length=14, verbose_name="CPF Testemunha 1")
    testemunha2_name = models.CharField(max_length=255, verbose_name="Nome Testemunha 2", default="")
    testemunha2_cpf = models.CharField(max_length=14, verbose_name="CPF Testemunha 2")
    
    signature_city = models.CharField(max_length=100, default='Rio de Janeiro', verbose_name="Cidade da Assinatura")
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_security_deposit(self):
        return self.monthly_value * self.security_deposit_months

    def __str__(self):
        return f"Contrato {self.id} - {self.tenant_name}"

class ContractDocument(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='documents')
    
    file = models.FileField(
        upload_to='contract_docs/',
        verbose_name="Arquivo"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc {self.id} - {self.contract.tenant_name}"
