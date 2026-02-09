# SAC - Sistema de Automação de Contratos

O **SAC** é uma aplicação web desenvolvida para padronizar a emissão de contratos de locação. O sistema permite que um utilizador preencha informações variáveis através de um formulário e gere, instantaneamente, um documento PDF formatado de acordo com um modelo jurídico pré-estabelecido.

## 🚀 Objetivos Principais
* Eliminar erros de digitação em cláusulas padrão.
* Centralizar a gestão de contratos emitidos.
* Garantir praticidade e rapidez na geração de documentos jurídicos.

## ✨ Funcionalidades
- **Gestão de Dados**: Interface intuitiva para inserção de dados do Locador, Locatário, Imóvel e Condições Financeiras.
- **Motor de Templates**: Processamento de modelos dinâmicos via Django Template Engine.
- **Geração de PDF**: Conversão de HTML/CSS para PDF de alta qualidade usando **WeasyPrint**.
- **Regras de Negócio Inclusas**:
    - Cálculo automático de multa rescisória *pro-rata* para contratos típicos.
    - Parcelamento automático de garantia caução.
- **Histórico**: Listagem e consulta de contratos gerados.
- **CI/CD**: Pipeline automatizado via GitHub Actions para garantir a qualidade do código.

## 🛠️ Stack Tecnológica
* **Backend**: Python 3.11+ / Django 4.2+
* **Database**: PostgreSQL
* **PDF Engine**: WeasyPrint
* **Frontend**: Django Templates + Tailwind CSS
* **Container**: Docker & Docker Compose
* **CI/CD**: GitHub Actions

## 📂 Estrutura do Projeto
```text
.
├── core/               # Configurações globais Django
├── contracts/          # Aplicação principal (Models, Views, Forms)
│   ├── services/       # Lógica de negócio (Cálculos de multa, etc.)
│   ├── tests/          # Testes automatizados
│   └── templates/      # Templates HTML de interface e PDF
├── generator/          # Módulo isolado para renderização de PDF
├── .github/workflows/  # Pipeline de CI/CD
├── Dockerfile          # Definição da imagem principal
└── docker-compose.yml  # Orquestração do ambiente de desenvolvimento
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
   ```bash
   docker compose up -d
   ```
   > **Nota:** Utilize a flag `--build` apenas se houver alterações no `Dockerfile` ou em `requirements.txt`. Para alterações de código/templates, o volume montado já reflete as mudanças automaticamente.

3. Execute as migrações do banco de dados:
   ```bash
   docker compose exec web python manage.py migrate
   ```

4. Acesse a aplicação em: [http://localhost:8000](http://localhost:8000)

## 🧪 Testes
Para rodar a suíte de testes automatizados:
```bash
docker compose exec web python manage.py test contracts
```

## 📄 Notas de Refatoração
O projeto foi recentemente refatorado para alinhar-se à especificação técnica original (`SPEC.md`), isolando a lógica de geração de PDF no módulo `generator` e padronizando as configurações no diretório `core`.
