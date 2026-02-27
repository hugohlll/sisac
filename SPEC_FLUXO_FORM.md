# **Especificação Técnica: Fluxo de Solicitação Web (Fluxo Nativo)**

**Projeto:** SISAC \- Sistema de Automação de Contratos

**Data:** 10/02/2026

**Status:** Planejamento Atualizado (Com Arquitetura de Nuvem Definida)

## **1\. Contexto e Objetivo**

O objetivo é permitir que o próprio locatário inicie o processo de locação através de uma página web pública hospedada no próprio sistema. Além dos dados cadastrais, o sistema deve permitir o envio de documentos comprobatórios (identidade, comprovante de renda).

**Fluxo Proposto:**

1. **Locatário (Público):** Acessa URL pública, preenche dados e anexa documentos.  
2. **Sistema:** Valida dados, faz upload transparente para nuvem (Cloudinary), cria registro PENDENTE.  
3. **Locador (Admin):** Recebe notificação, acessa o registro e clica nos links para conferir os documentos.  
4. **Locador (Conclusão):** Aprova, preenche dados restantes e gera o contrato.

## **2\. Diretrizes Técnicas e Manutenibilidade**

1. **Herança de Formulários (DRY):**  
   * Manter o uso de ContractForm como base.  
   * Lógica de validação de arquivos deve ser modular (validators.py).  
2. **Arquitetura de Armazenamento (Híbrida):**  
   * **Arquivos Estáticos (CSS/JS):** Continuar utilizando **WhiteNoise**. É a solução mais performática para o Render e já está configurada e funcional.  
   * **Arquivos de Mídia (Uploads):** Utilizar **Cloudinary** (Plano Gratuito).  
   * **Justificativa:** O container do Render tem sistema de arquivos efêmero (arquivos são deletados ao reiniciar). O Cloudinary persiste esses arquivos externamente via API, sem ocupar espaço no banco de dados Neon.

## **3\. Alterações no Banco de Dados (contracts/models.py)**

Ajustes no modelo para suportar status e relação de documentos.

\# contracts/models.py  
from django.db import models  
from django.core.validators import FileExtensionValidator

class Contract(models.Model):  
    \# ... campos existentes mantidos ...

    STATUS\_CHOICES \= \[  
        ('PENDING', 'Pendente de Análise'),  
        ('APPROVED', 'Aprovado/Finalizado'),  
        ('REJECTED', 'Rejeitado'),  
    \]  
    status \= models.CharField(  
        max\_length=10,   
        choices=STATUS\_CHOICES,   
        default='PENDING',  
        verbose\_name="Status"  
    )

    \# Campos tornados OPCIONAIS (null=True, blank=True) para permitir cadastro parcial:  
    locadora\_nome \= models.CharField(..., null=True, blank=True)  
    locadora\_cpf \= models.CharField(..., null=True, blank=True)  
    locadora\_rg \= models.CharField(..., null=True, blank=True)  
    locadora\_endereco \= models.CharField(..., null=True, blank=True)  
      
    property\_address \= models.TextField(..., null=True, blank=True)  
    property\_cep \= models.CharField(..., null=True, blank=True)  
      
    monthly\_value \= models.DecimalField(..., null=True, blank=True)  
    start\_date \= models.DateField(..., null=True, blank=True)  
    \# Ajustar demais campos financeiros para aceitar null se não tiverem default

\# NOVO MODELO DE DOCUMENTOS  
class ContractDocument(models.Model):  
    contract \= models.ForeignKey(Contract, on\_delete=models.CASCADE, related\_name='documents')  
      
    \# O Cloudinary ignorará o caminho físico, mas usará 'contract\_docs' como "folder" na dashboard deles  
    file \= models.FileField(  
        upload\_to='contract\_docs/',  
        verbose\_name="Arquivo"  
    )  
    uploaded\_at \= models.DateTimeField(auto\_now\_add=True)

    def \_\_str\_\_(self):  
        return f"Doc {self.id} \- {self.contract.tenant\_name}"

## **4\. Implementação do Backend**

### **4.1. Configuração do Storage (core/settings.py e requirements.txt)**

A migração para Cloudinary exige apenas configuração, sem mudança de lógica de negócio.

**Requirements (requirements.txt):**

Adicionar:

cloudinary  
django-cloudinary-storage

**Settings (core/settings.py):**

import os

INSTALLED\_APPS \= \[  
    \# ...  
    'cloudinary\_storage', \# Deve estar acima de 'django.contrib.staticfiles'  
    'django.contrib.staticfiles',  
    'cloudinary',  
    \# ...  
\]

\# Configuração Cloudinary (Lê do ambiente do Render)  
CLOUDINARY\_STORAGE \= {  
    'CLOUD\_NAME': os.environ.get('CLOUDINARY\_CLOUD\_NAME'),  
    'API\_KEY': os.environ.get('CLOUDINARY\_API\_KEY'),  
    'API\_SECRET': os.environ.get('CLOUDINARY\_API\_SECRET'),  
}

\# ARQUITETURA HÍBRIDA:  
\# 1\. Media (Uploads) \-\> Vai para o Cloudinary  
DEFAULT\_FILE\_STORAGE \= 'cloudinary\_storage.storage.MediaCloudinaryStorage'

\# 2\. Static (CSS/JS) \-\> Continua no WhiteNoise (Render)  
STATICFILES\_STORAGE \= "whitenoise.storage.CompressedManifestStaticFilesStorage"

### **4.2. Validadores (contracts/validators.py)**

Criar arquivo para validação de segurança e consistência.

from django.core.exceptions import ValidationError  
import os

def validate\_file\_size(value):  
    limit \= 5 \* 1024 \* 1024  \# 5 MB  
    if value.size \> limit:  
        raise ValidationError('O arquivo não pode exceder 5MB.')

def validate\_file\_extension(value):  
    ext \= os.path.splitext(value.name)\[1\]  
    valid\_extensions \= \['.pdf', '.jpg', '.jpeg', '.png'\]  
    if not ext.lower() in valid\_extensions:  
        raise ValidationError('Formato não suportado. Use PDF, JPG ou PNG.')

### **4.3. Formulário do Locatário (contracts/forms.py)**

Uso de ContractForm como base para herdar validações de CPF e dados comuns.

\# contracts/forms.py  
from django import forms  
from .models import Contract  
from .validators import validate\_file\_size, validate\_file\_extension

class TenantSolicitationForm(ContractForm):  
    documents \= forms.FileField(  
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  
        label="Documentos (Identidade, Renda)",  
        required=False,  
        help\_text="Formatos: PDF, JPG, PNG. Máx: 5MB por arquivo."  
    )

    class Meta(ContractForm.Meta):  
        model \= Contract  
        \# Apenas campos que o inquilino preenche  
        fields \= \[  
            'tenant\_name', 'tenant\_cpf', 'tenant\_rg',   
            'tenant\_profession', 'tenant\_prev\_address',   
            'documents'  
        \]

    def clean\_documents(self):  
        files \= self.files.getlist('documents')  
        if len(files) \> 5:  
            raise ValidationError("Máximo de 5 arquivos permitidos.")  
          
        for f in files:  
            validate\_file\_size(f)  
            validate\_file\_extension(f)  
        return files

### **4.4. Views (contracts/views.py)**

A view intercepta o upload e cria os registros. O upload físico é transparente.

\# contracts/views.py  
from .models import Contract, ContractDocument  
from .forms import TenantSolicitationForm

class PublicSolicitationCreateView(CreateView):  
    model \= Contract  
    form\_class \= TenantSolicitationForm  
    template\_name \= 'contracts/public\_solicitation\_form.html'  
      
    def form\_valid(self, form):  
        \# 1\. Salva o Contrato (Pai)  
        self.object \= form.save(commit=False)  
        self.object.status \= 'PENDING'  
        self.object.save()  
          
        \# 2\. Processa os Arquivos  
        \# O Django recebe os arquivos e o Storage Backend (Cloudinary)  
        \# faz o upload automaticamente quando chamamos .create() no FileField  
        files \= self.request.FILES.getlist('documents')  
        for f in files:  
            ContractDocument.objects.create(contract=self.object, file=f)  
              
        return super().form\_valid(form)

    def get\_success\_url(self):  
        return reverse\_lazy('solicitation-success')

## **5\. Templates e Frontend**

### **5.1. Formulário Público (public\_solicitation\_form.html)**

* **Crucial:** O formulário HTML deve conter enctype="multipart/form-data".  
* Design minimalista focado no locatário.

### **5.2. Área do Locador (contract\_form.html)**

* Exibir a lista de documentos apenas em modo de edição/revisão.  
* Os links gerados por {{ doc.file.url }} apontarão automaticamente para https://res.cloudinary.com/....

{% if contract.documents.exists %}  
\<div class="bg-blue-50 p-4 rounded-lg border border-blue-200 mb-6"\>  
    \<h3 class="font-bold text-gray-700 mb-2"\>Documentos do Inquilino:\</h3\>  
    \<ul class="list-disc pl-5"\>  
        {% for doc in contract.documents.all %}  
        \<li\>  
            \<a href="{{ doc.file.url }}" target="\_blank" class="text-blue-600 hover:underline"\>  
                Abrir Documento {{ forloop.counter }}  
            \</a\>  
        \</li\>  
        {% endfor %}  
    \</ul\>  
\</div\>  
{% endif %}

## **6\. Plano de Execução**

1. **Cloudinary:** Criar conta Free e pegar credenciais.  
2. **Variáveis de Ambiente (Render):** Adicionar CLOUDINARY\_CLOUD\_NAME, CLOUDINARY\_API\_KEY, CLOUDINARY\_API\_SECRET.  
3. **Código:** Implementar Models, Forms e Configurações conforme especificado acima.  
4. **Deploy:** Fazer push para o GitHub. O Render detectará a mudança, instalará as novas bibliotecas e rodará as migrações.