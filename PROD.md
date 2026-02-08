# **Documentação do Sistema de Automação de Contratos (SAC)**

## **1\. Visão Geral e Finalidade**

O **SAC** é uma aplicação web desenvolvida para padronizar a emissão de contratos de locação. O sistema permite que um utilizador preencha informações variáveis através de um formulário e gere, instantaneamente, um documento PDF formatado de acordo com um modelo jurídico pré-estabelecido.

### **Objetivos Principais:**

* Eliminar erros de digitação em cláusulas padrão.  
* Centralizar a gestão de contratos emitidos.  
* Garantir custo zero de manutenção para baixo volume de uso.

## **2\. Escopo do Projeto**

### **Funcionalidades (MVP):**

* **Gestão de Dados:** Interface para inserção de dados do Locador, Locatário, Imóvel e Condições Financeiras.  
* **Motor de Templates:** Processamento de modelos HTML (**TEMPL.md**) com variáveis dinâmicas via Django Template Engine.  
* **Geração de PDF:** Conversão de HTML/CSS para PDF de alta qualidade usando **WeasyPrint**.  
* **Histórico Simples:** Listagem de contratos gerados para consulta posterior.

### **Regras de Negócio Específicas (Consolidadas):**

* **Rescisão \- Contrato Típico (30 meses):** \* **Período de Carência:** 12 meses.  
  * **Isenção de Multa:** Somente após o 12º mês completo, com aviso prévio de 30 dias.  
  * **Multa Antecipada (Antes do 12º mês):** O locatário deverá pagar o montante equivalente à **soma dos aluguéis restantes** para completar o 12º mês de contrato (calculado *pro-rata die*).  
* **Garantia Locatícia (Depósito Caução):** \* **Valor:** Definido por multiplicador (padrão 3 meses).  
  * **Forma de Pagamento:** À Vista ou Parcelado (1.5 aluguel na assinatura \+ 0.5 aluguel no 2º mês).  
* **Encargos Adicionais:** Suporte para Taxa de Manutenção fixa e definição de cobrança de Utilidade Pública (Água/Luz) como fixo, percentual ou incluso.

## **3\. Arquitetura e Infraestrutura**

| **Camada** | **Tecnologia** | **Descrição** |

| **Linguagem** | Python 3.11+ | Lógica de backend e processamento. |

| **Framework** | Django 4.2+ | Gestão de rotas, banco de dados e templates. |

| **Base de Dados** | PostgreSQL (Neon.tech) | Persistência de dados dos contratos. |

| **Motor de PDF** | WeasyPrint | Renderização de HTML/CSS para PDF. |

| **Hospedagem** | Render.com | Deploy automatizado via GitHub. |

## **4\. Modelo de Dados (Entidade Contract)**

Para suportar o template definido em **TEMPL.md**, a entidade de contrato deve conter:

* **Locação:** contract\_type (TIPICO/ATIPICO), duration\_months, start\_date, justification\_atipico.  
* **Partes:** Dados completos (Nome, CPF, RG, Endereço) de Locador, Locatário e Testemunhas.  
* **Valores:** monthly\_value, payment\_day, maintenance\_fee.  
* **Caução:** security\_deposit\_months, security\_deposit\_payment\_type.  
* **Serviços:** water\_billing\_type, power\_billing\_type, water\_description, power\_description.

## **5\. Estrutura do Contrato (Referência TEMPL.md)**

O sistema utiliza um template padronizado dividido nas seguintes seções:

1. **Qualificação das Partes** (Identificação civil completa).  
2. **Objeto e Vigência** (Dados do imóvel e prazo contratual).  
3. **Aluguel e Encargos** (Valores financeiros e modalidade de caução).  
4. **Utilidade Pública** (Regras para Água e Energia).  
5. **Benfeitorias e Vistorias** (Normas de conservação e Anexo I).  
6. **Rescisão e Multa** (Lógica diferenciada para contratos típicos/atípicos).  
7. **Disposições Finais** (Assinaturas e validade jurídica eletrônica).

## **6\. Próximos Passos**

1. \~\~Configuração das Especificações Técnicas (SPEC.md)\~\~.  
2. \~\~Definição do Template Base (TEMPL.md)\~\~.  
3. Criação do arquivo styles.css para formatação profissional do PDF.  
4. Implementação do App Django (Models, Views e Forms).  
5. Criação da interface de formulário baseada em Tailwind CSS.