# Template de Contrato de Locação (Atualizado v4.5)

Baseado no script `contratos.ipynb`.

## 1. QUALIFICAÇÃO
**LOCADORA:** {{ locadora_nome }}, nacionalidade brasileira, CPF: {{ locadora_cpf }}, RG: {{ locadora_rg }}, residente: {{ locadora_endereco }}.
**LOCATÁRIO(A):** {{ tenant_name }}, nacionalidade BRASILEIRA, CPF: {{ tenant_cpf }}, RG: {{ tenant_rg }}, Profissão: {{ tenant_profession }}, Endereço anterior: {{ tenant_prev_address }}.

Imóvel: {{ property_address }}, CEP: {{ property_cep }}.
Prazo: {{ duration_months }} meses (Típico: 30 meses).
{% if ATIPICO %} Justificativa: {{ justification_atipico }} {% endif %}

## 2. ALUGUEL E ENCARGOS
Valor: R$ {{ monthly_value }}, dia {{ payment_day }}.
Taxa Manutenção: {{ maintenance_fee }} (se houver).
Caução: R$ {{ total_security_deposit }} ({{ security_deposit_months }} meses).
Pagamento Caução: {{ security_deposit_payment_type }} (À vista ou Parcelado em 1.5x + 0.5x).

IPCA anual. Multa 10% atraso. Despejo após 25 dias inadimplência.

## 3. CLÁUSULAS GERAIS
**Utilidades:**
- Água: {{ water_billing_type }} (Fixo/Conta Individual/Incluso).
- Luz: {{ power_billing_type }} (Fixo/Conta Individual/Incluso).
- Proibição de resistências elétricas.

**Rescisão:**
- Típico (30 meses): Sem multa após 12 meses (aviso 30 dias). Antes de 12 meses: Multa 1 aluguel proporcional.
- Atípico (<30 meses): Multa 1 aluguel proporcional ao restante. Aviso 30 dias.

**Benfeitorias e Vistorias:**
- Anexo I (Fotos).
- Vistoria entrada/saída.
- Proibição de alterações sem autorização.

**Entrega Chaves:** 5 dias para retirada.

**Regras Convivência:** Respeito ao regimento.

**Devolução Imóvel:** Restituição nas mesmas condições. 7 dias para reparos ou uso do depósito.

**Disposições Finais:** Cadastro atualizado. Assinatura eletrônica (ICP-Brasil/Docusign) válida.

## 4. ASSINATURAS
Local/Data.
Locadora, Locatário, 2 Testemunhas.