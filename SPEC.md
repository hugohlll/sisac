# **Especificação Técnica: Sistema de Automação de Contratos (SAC)**

Este documento detalha os requisitos técnicos e a lógica de implementação do sistema, alinhando o modelo de dados às regras de negócio, arquitetura e processos de qualidade.

## **1\. Stack Tecnológica**

* **Backend:** Python 3.11+ / Django 4.2+.  
* **Database:** PostgreSQL (Hospedado via Neon.tech).  
* **PDF Engine:** WeasyPrint (estilização via CSS3 e templates HTML).  
* **Hospedagem:** Render.com (Web Service Free).  
* **Frontend:** Django Templates \+ Tailwind CSS.

## **2\. Modelo de Dados (ORM)**

O modelo Contract reflete os campos necessários para preencher o TEMPL.md:

from django.db import models  
import uuid

class Contract(models.Model):  
    id \= models.UUIDField(primary\_key=True, default=uuid.uuid4, editable=False)  
      
    \# Dados da Locadora  
    locadora\_nome \= models.CharField(max\_length=255)  
    locadora\_cpf \= models.CharField(max\_length=14)  
    locadora\_rg \= models.CharField(max\_length=20)  
    locadora\_endereco \= models.CharField(max\_length=255)  
      
    \# Dados do Locatário  
    tenant\_name \= models.CharField(max\_length=255)  
    tenant\_cpf \= models.CharField(max\_length=14)  
    tenant\_rg \= models.CharField(max\_length=20)  
    tenant\_profession \= models.CharField(max\_length=100)  
    tenant\_prev\_address \= models.TextField()  
      
    \# Dados do Imóvel  
    property\_address \= models.TextField()  
    property\_cep \= models.CharField(max\_length=9)  
      
    \# Financeiro e Prazos  
    monthly\_value \= models.DecimalField(max\_digits=10, decimal\_places=2)  
    payment\_day \= models.PositiveIntegerField(default=10)  
    start\_date \= models.DateField()  
    duration\_months \= models.PositiveIntegerField(default=30)  
    contract\_type \= models.CharField(  
        max\_length=10,   
        choices=\[('TIPICO', 'Típico'), ('ATIPICO', 'Atípico')\]  
    )  
    justification\_atipico \= models.TextField(null=True, blank=True)  
      
    \# Garantia  
    security\_deposit\_months \= models.PositiveIntegerField(default=3)  
    security\_deposit\_payment\_type \= models.CharField(  
        max\_length=20,   
        choices=\[('VISTA', 'À Vista'), ('PARCELADO', 'Parcelado')\]  
    )  
      
    \# Encargos Extras  
    maintenance\_fee \= models.DecimalField(max\_digits=10, decimal\_places=2, default=0)  
    water\_billing\_type \= models.CharField(max\_length=20)   
    water\_description \= models.CharField(max\_length=255)  
    power\_billing\_type \= models.CharField(max\_length=20)   
    power\_description \= models.CharField(max\_length=255)  
      
    testemunha1\_cpf \= models.CharField(max\_length=14)  
    testemunha2\_cpf \= models.CharField(max\_length=14)  
      
    created\_at \= models.DateTimeField(auto\_now\_add=True)

    @property  
    def total\_security\_deposit(self):  
        return self.monthly\_value \* self.security\_deposit\_months

## **3\. Lógica de Negócio (Backend)**

### **3.1 Cálculo de Multa (Rescisão Típica)**

Localizado em contracts/services/calculator.py:

* Se contract\_type \== 'TIPICO':  
  * Meses decorridos \< 12: Multa \= (12 \- meses\_decorridos) \* monthly\_value (pro-rata).  
  * Meses decorridos \>= 12: Multa \= 0 (após aviso de 30 dias).

### **3.2 Parcelamento de Caução**

* 'PARCELADO': Parcela 1 (1.5x) e Parcela 2 (0.5x).

## **4\. Estrutura de Diretórios**

sac\_project/  
├── core/                   \# Configurações globais Django  
├── contracts/              \# App principal  
│   ├── services/           \# Lógica (calculator.py, data\_cleaner.py)  
│   ├── tests/              \# Testes automatizados (pytest)  
│   ├── models.py  
│   └── views.py  
├── generator/              \# Engine de PDF  
├── .github/  
│   └── workflows/          \# CI/CD (GitHub Actions)  
├── requirements.txt  
└── Dockerfile

## **5\. Testes Automatizados**

Para garantir a integridade das cláusulas financeiras, utilizaremos o framework pytest.

### **5.1 Níveis de Teste**

* **Unitários (Services):** Validar cálculos de multa pro-rata e parcelamento de caução em calculator.py.  
* **Integração (Models):** Garantir que o modelo Contract salva e recupera os dados corretamente do PostgreSQL.  
* **Funcionais (PDF):** Verificar se a View de geração de contrato retorna um status 200 OK e um Content-Type: application/pdf.

### **5.2 Ferramentas**

* pytest-django: Integração do pytest com o ambiente Django.  
* model-bakery: Para criação rápida de instâncias de teste sem boilerplate.

## **6\. CI/CD (Integração e Entrega Contínua)**

O pipeline será executado via **GitHub Actions** em cada *Push* ou *Pull Request* para o branch main.

### **6.1 Estágios do Pipeline**

1. **Linting & Formatação:** Execução do flake8 ou black para garantir padrões de código.  
2. **Testes Automatizados:** Execução do pytest com banco de dados em memória (SQLite para testes rápidos ou Postgres via Service Container).  
3. **Build:** Verificação de construção da imagem Docker (opcional).  
4. **Deploy:** Acionamento do Webhook do Render.com para deploy automático após aprovação nos testes.

### **6.2 Configuração de Ambiente (Secrets)**

As chaves sensíveis devem ser armazenadas no GitHub Secrets:

* DJANGO\_SECRET\_KEY  
* DATABASE\_URL (para testes de integração se necessário)  
* RENDER\_DEPLOY\_HOOK

## **7\. Infraestrutura**

* **WhiteNoise:** Gestão de arquivos estáticos.  
* **Gunicorn:** Servidor de produção.  
* **Render.com:** Deploy via integração direta com o GitHub (Auto-deploy on green build).