# SAC - Sistema de Automação de Contratos

O **SAC** é uma aplicação web desenvolvida para padronizar a emissão de contratos de locação. O sistema permite que um utilizador preencha informações variáveis através de um formulário e gere, instantaneamente, um documento PDF formatado de acordo com um modelo jurídico pré-estabelecido.

## 🚀 Objetivos Principais
* Eliminar erros de digitação em cláusulas padrão.
* Centralizar a gestão de contratos emitidos.
* Garantir praticidade e rapidez na geração de documentos jurídicos.
* Permitir que locatários solicitem contratos de forma autônoma via formulário público.

## ✨ Funcionalidades

### Gestão de Contratos (Área do Locador)
- **Criação de Contratos**: Formulário completo para inserção dos dados do Locador, Locatário, Imóvel, Condições Financeiras, Testemunhas e Encargos.
- **Listagem e Consulta**: Histórico de contratos gerados, ordenados por status (`Pendente` primeiro) e data de criação.
- **Edição de Contratos**: Edição completa de contratos existentes, com aprovação automática ao salvar.
- **Geração de PDF**: Conversão de HTML/CSS para PDF de alta qualidade usando **WeasyPrint**, com formatação automática de CPF e CEP.

### Regras de Negócio
- **Cálculo de Multa Rescisória**: Cálculo automático *pro-rata* para contratos típicos (meses restantes × valor mensal se < 12 meses).
- **Parcelamento de Garantia Caução**: Geração automática de parcelas quando aplicável.
- **Validação de CPF/CEP**: Limpeza e formatação automática de campos de documento.
- **Validação de Valores Monetários**: Conversão do formato brasileiro (1.234,56) para Decimal.

### Formulário Público de Solicitação (`/solicitar/`)
- **Acesso Público**: Locatários podem enviar seus dados sem necessidade de login.
- **Upload de Documentos**: Envio de até 5 arquivos (PDF, JPG, PNG — máx. 5MB cada) com validação de tipo e tamanho.
- **Status de Acompanhamento**: Solicitações são criadas com status `PENDENTE` e podem ser Aprovadas ou Rejeitadas pelo locador.
- **Página de Confirmação**: Após o envio, o locatário recebe uma confirmação visual.

### Administração
- **Django Admin**: Painel administrativo com listagem, busca e filtros por tipo, status e dia de pagamento.
- **Documentos Inline**: Visualização dos documentos enviados pelo locatário diretamente no detalhe do contrato.

### Infraestrutura e DevOps
- **CI/CD**: Pipeline automatizado via **GitHub Actions** (`ci.yml`) com testes e build Docker.
- **Armazenamento Híbrido**: Estáticos via **WhiteNoise**, uploads de mídia via **Cloudinary** em produção (ou armazenamento local em dev).
- **Criação Automática de Superusuário**: Comando de management customizado para criação automática em deploy.

## 🛠️ Stack Tecnológica
| Camada      | Tecnologia                          |
|-------------|-------------------------------------|
| Backend     | Python 3.11+ / Django 4.2+         |
| Database    | PostgreSQL 15                       |
| PDF Engine  | WeasyPrint 60+                      |
| Frontend    | Django Templates + Tailwind CSS     |
| Container   | Docker & Docker Compose             |
| Produção    | Gunicorn + WhiteNoise + Cloudinary  |
| CI/CD       | GitHub Actions                      |

## 📂 Estrutura do Projeto
```text
.
├── core/                   # Configurações globais Django (settings, urls, wsgi)
├── contracts/              # Aplicação principal
│   ├── models.py           # Contract + ContractDocument
│   ├── views.py            # CRUD + Solicitação Pública + PDF
│   ├── forms.py            # ContractForm + TenantSolicitationForm
│   ├── validators.py       # Validação de arquivos (tamanho e extensão)
│   ├── admin.py            # ContractAdmin + DocumentInline
│   ├── services/           # Lógica de negócio (calculator.py)
│   ├── tests/              # Testes automatizados
│   └── templates/          # Templates HTML (formulários, lista, PDF)
├── generator/              # Módulo isolado para renderização de PDF
├── .github/workflows/      # Pipeline de CI/CD (ci.yml)
├── Dockerfile              # Imagem de produção
├── docker-compose.yml      # Ambiente de desenvolvimento
├── requirements.txt        # Dependências Python
├── SPEC.md                 # Especificação técnica original
├── SPEC_FLUXO_FORM.md      # Especificação do fluxo de solicitação
└── MANUAL_DEV.md           # Manual do desenvolvedor
```

## ⚙️ Como Executar (Localmente via Docker)

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/hugohlll/sisac.git
   cd sisac
   ```

2. Suba o ambiente com Docker Compose:
   ```bash
   docker compose up -d
   ```
   > **Nota:** Utilize a flag `--build` apenas se houver alterações no `Dockerfile` ou em `requirements.txt`. Para alterações de código/templates, o volume montado já reflete as mudanças automaticamente.

3. Execute as migrações do banco de dados:
   ```bash
   docker compose exec web python manage.py migrate
   ```

4. (Opcional) Crie um superusuário para acessar o admin:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. Acesse a aplicação:
   | Página                      | URL                                    |
   |-----------------------------|----------------------------------------|
   | Formulário de Contrato      | http://localhost:8000                   |
   | Lista de Contratos          | http://localhost:8000/list/             |
   | Solicitação Pública         | http://localhost:8000/solicitar/        |
   | Painel Administrativo       | http://localhost:8000/admin/            |

## 🧪 Testes
Para rodar a suíte de testes automatizados:
```bash
docker compose exec web python manage.py test contracts
```

### Testes Disponíveis
- **`test_calculator.py`**: Testes unitários para cálculos de multa rescisória.
- **`test_pdf_generation.py`**: Testes de integração para geração de PDF (status 200, content-type, etc.).

## 📄 Documentação Adicional
- **[SPEC.md](SPEC.md)** — Especificação técnica completa do sistema.
- **[SPEC_FLUXO_FORM.md](SPEC_FLUXO_FORM.md)** — Especificação do fluxo de solicitação pública com upload de documentos.
- **[MANUAL_DEV.md](MANUAL_DEV.md)** — Manual de desenvolvimento e manutenção.
