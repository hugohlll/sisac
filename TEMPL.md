# **Template Base do Contrato de Locação**

Este arquivo define a estrutura textual que será processada pelo Django para gerar o PDF via WeasyPrint.

## **CONTRATO DE LOCAÇÃO RESIDENCIAL**

### **1\. QUALIFICAÇÃO DAS PARTES**

**LOCADORA:** {{ locadora\_nome }}, nacionalidade brasileira, estado civil casada, CPF: {{ locadora\_cpf }}, RG: {{ locadora\_rg }}, residente e domiciliada no endereço: {{ locadora\_endereco }}.

**LOCATÁRIO(A):** {{ tenant\_name }}, nacionalidade brasileira, CPF: {{ tenant\_cpf }}, RG: {{ tenant\_rg }}, profissão: {{ tenant\_profession }}, residente anteriormente em: {{ tenant\_prev\_address }}.

### **2\. DO OBJETO E DA VIGÊNCIA**

O imóvel de propriedade da LOCADORA situa-se no endereço: {{ property\_address }}, CEP: {{ property\_cep }}.

O prazo de locação terá validade de **{{ duration\_months }} meses**, iniciando em {{ start\_date|date:"d/m/Y" }}.

{% if contract\_type \== 'ATIPICO' %}

O presente contrato é celebrado com prazo inferior a 30 meses em razão de se destinar a {{ justification\_atipico }}, em conformidade com a legislação aplicável.

{% endif %}

A presente LOCAÇÃO destina-se exclusivamente ao uso residencial.

### **3\. ALUGUEL E ENCARGOS LOCATÍCIOS**

O(A) locatário(a) pagará o valor de **R$ {{ monthly\_value }}** referente ao aluguel, com vencimento todo dia **{{ payment\_day }}** de cada mês, referente ao mês vincendo.

{% if maintenance\_fee \> 0 %}

Adicionalmente, será cobrada uma taxa de manutenção das áreas comuns no valor fixo de **R$ {{ maintenance\_fee }}**, paga mensalmente junto ao aluguel.

{% endif %}

**Garantia Locatícia:** Será depositado a título de caução o valor de **R$ {{ total\_security\_deposit }}** (equivalente a {{ security\_deposit\_months }} meses de aluguel).

{% if security\_deposit\_payment\_type \== 'VISTA' %}

O pagamento integral do depósito será realizado no ato da assinatura.

{% else %}

O pagamento será parcelado: R$ {{ deposit\_p1 }} no ato da assinatura e R$ {{ deposit\_p2 }} no segundo mês de vigência.

{% endif %}

O reajuste será anual com base no IPCA. Em caso de atraso, incidirá multa de 10% sobre o débito. A inadimplência superior a 25 dias resultará em rescisão imediata e desocupação.

### **4\. UTILIDADE PÚBLICA (ÁGUA E ENERGIA)**

{% if water\_billing\_type \== 'INCLUSO' and power\_billing\_type \== 'INCLUSO' %}

Não haverá cobrança de taxas de consumo de água ou energia elétrica, estando inclusos no valor do aluguel.

{% else %}

Os serviços serão cobrados da seguinte forma:

* **Água:** {{ water\_description }}  
* **Energia:** {{ power\_description }}  
  {% endif %}

Fica proibido o uso de aparelhos elétricos com resistência (ex: aquecedores). O descumprimento gera multa de 1 aluguel.

### **5\. BENFEITORIAS E VISTORIAS**

As condições do imóvel na entrada estão detalhadas no **Anexo I \- Vistoria de Entrada**. Qualquer divergência deve ser apontada em 5 dias. Benfeitorias dependem de autorização prévia por escrito e não geram direito a retenção ou indenização. O(A) locatário(a) deve reparar danos causados por si ou visitantes.

### **6\. RESCISÃO E MULTA CONTRATUAL**

{% if contract\_type \== 'TIPICO' %}

**Contrato Típico (30 meses):**

Ao(À) LOCATÁRIO(A) é facultada a rescisão unilateral após transcorridos **12 (doze) meses** de vigência, com isenção de multa, mediante aviso prévio de 30 dias.

Caso a rescisão ocorra **antes do 12º mês**, o(a) LOCATÁRIO(A) deverá pagar multa equivalente ao **somatório dos aluguéis restantes para completar o 12º mês de contrato** (calculado *pro-rata die*), valor este que poderá ser descontado da garantia.

{% else %}

**Contrato Atípico:**

Em caso de rescisão antecipada, incidirá multa contratual proporcional ao período restante do contrato, mediante aviso prévio de 30 dias.

{% endif %}

### **7\. DISPOSIÇÕES FINAIS E ASSINATURAS**

As partes aceitam assinaturas eletrônicas via plataformas autorizadas pela ICP-Brasil.

{{ cidade\_assinatura }}, {{ data\_assinatura }}.

**{{ locadora\_nome }}** (LOCADORA)

**{{ tenant\_name }}** (LOCATÁRIO/A)

**Testemunhas:**

1. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ CPF: {{ testemunha1\_cpf }}  
2. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ CPF: {{ testemunha2\_cpf }}