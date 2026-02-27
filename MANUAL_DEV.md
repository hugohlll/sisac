# Manual de Desenvolvimento e Manutenção

Este documento descreve os procedimentos padrão para realizar modificações no código e verificar o funcionamento do sistema **SAC (Sistema de Automação de Contratos)**.

> [!IMPORTANT]
> **O sistema executa em ambiente Docker Compose.**
> Nunca tente executar testes, migrações ou scripts de gerenciamento diretamente no seu terminal local (host), pois as dependências e o banco de dados estão isolados nos containers.

## 1. Ambiente de Execução

O projeto utiliza **Docker Compose** para orquestrar os serviços:

| Serviço | Container       | Descrição                |
|---------|-----------------|--------------------------|
| Web     | `sisac-web-1`   | Django (dev server)      |
| DB      | `sisac-db-1`    | PostgreSQL 15-alpine     |

### Comandos Essenciais
```bash
# Verificar containers em execução
docker ps

# Subir o ambiente
docker compose up -d

# Subir com rebuild (após mudanças no Dockerfile ou requirements.txt)
docker compose up -d --build

# Ver logs em tempo real
docker compose logs -f web

# Parar o ambiente
docker compose down
```

## 2. Estrutura do Código

### Arquitetura Geral

| Diretório / Arquivo     | Responsabilidade                                     |
|--------------------------|------------------------------------------------------|
| `core/`                  | Configurações Django (settings, urls, wsgi)         |
| `contracts/models.py`    | Modelos `Contract` e `ContractDocument`              |
| `contracts/views.py`     | Views de CRUD, Solicitação Pública e geração de PDF |
| `contracts/forms.py`     | `ContractForm` (admin) e `TenantSolicitationForm` (público) |
| `contracts/validators.py`| Validadores de arquivo (tamanho e extensão)         |
| `contracts/admin.py`     | Configuração do Django Admin                        |
| `contracts/services/`    | Lógica de negócio (calculator.py)                   |
| `contracts/tests/`       | Testes automatizados                                |
| `contracts/templates/`   | Templates HTML (formulários, lista, PDF)            |
| `generator/`             | Motor de renderização de PDF com WeasyPrint         |

### URLs e Rotas

| URL                         | View                           | Descrição                          |
|-----------------------------|--------------------------------|------------------------------------|
| `/`                         | `ContractCreateView`           | Criação de contrato (admin)        |
| `/list/`                    | `ContractListView`             | Lista de contratos                 |
| `/edit/<uuid:pk>/`          | `ContractUpdateView`           | Edição de contrato                 |
| `/solicitar/`               | `PublicSolicitationCreateView` | Formulário público do locatário    |
| `/solicitacao-concluida/`   | `SolicitationSuccessView`      | Confirmação de solicitação         |
| `/contract/<uuid:pk>/pdf/`  | `generate_pdf`                 | Geração do PDF do contrato         |
| `/documento/<int:pk>/`      | `serve_document`               | Servir documento enviado           |
| `/admin/`                   | Django Admin                   | Painel administrativo              |

## 3. Fluxo de Modificação de Código

1. **Planejamento**: Identifique os arquivos e o impacto das mudanças.
2. **Edição**: Edite os arquivos no seu ambiente local (host). O volume Docker está mapeado, então as alterações refletem imediatamente no container.
3. **Verificação**: Após editar, **sempre** execute os testes para validar a alteração.

## 4. Verificação e Testes

A etapa de verificação deve ocorrer **dentro do container**.

### Executando Testes

```bash
# Todos os testes
docker compose exec web python manage.py test contracts

# Teste específico
docker compose exec web python manage.py test contracts.tests.test_calculator
docker compose exec web python manage.py test contracts.tests.test_pdf_generation
```

### Testes Disponíveis

| Arquivo                 | Cobertura                                               |
|-------------------------|---------------------------------------------------------|
| `test_calculator.py`    | Cálculos de multa rescisória pro-rata                   |
| `test_pdf_generation.py`| Geração de PDF (status 200, content-type application/pdf)|

> [!WARNING]
> Se você tentar rodar `python manage.py test` diretamente no host, receberá erros de dependências não encontradas (como `dj_database_url`) ou conexão com banco de dados.

### Acessando o Shell do Container

```bash
docker compose exec -it web /bin/bash
# Uma vez dentro do container:
python manage.py shell
# ou
python manage.py test
```

## 5. Banco de Dados e Migrações

### Criando e Aplicando Migrações
```bash
# Criar uma nova migração após alterar models.py
docker compose exec web python manage.py makemigrations contracts

# Aplicar migrações
docker compose exec web python manage.py migrate
```

### Modelos Principais

**Contract** — Contrato de locação:
- Dados da Locadora (nome, CPF, RG, endereço)
- Dados do Locatário (nome, CPF, RG, profissão, endereço anterior)
- Dados do Imóvel (endereço, CEP)
- Financeiro (valor mensal, dia de pagamento, data de início, duração, tipo)
- Garantia (meses de caução, forma de pagamento)
- Encargos (manutenção, água, energia)
- Testemunhas (nome e CPF)
- Status (`PENDING`, `APPROVED`, `REJECTED`)

**ContractDocument** — Documentos do locatário:
- Relacionado ao contrato via `ForeignKey`
- Upload de arquivo (PDF, JPG, PNG — máx. 5MB)

## 6. Variáveis de Ambiente

### Desenvolvimento (docker-compose.yml)
As variáveis já estão pré-configuradas no `docker-compose.yml`.

### Produção
| Variável                  | Descrição                        |
|---------------------------|----------------------------------|
| `DEBUG`                   | Deve ser `0` ou `False`          |
| `DJANGO_SECRET_KEY`       | Chave secreta Django             |
| `DJANGO_ALLOWED_HOSTS`    | Hosts permitidos (separados por espaço) |
| `DATABASE_URL`            | URL do PostgreSQL (Neon.tech)    |
| `CLOUDINARY_CLOUD_NAME`   | Nome da cloud no Cloudinary      |
| `CLOUDINARY_API_KEY`      | API Key do Cloudinary            |
| `CLOUDINARY_API_SECRET`   | API Secret do Cloudinary         |

## 7. Deploy em Produção

O deploy é feito via **Render.com** com integração direta ao GitHub:

1. Push para o branch `main` aciona o pipeline CI/CD.
2. GitHub Actions roda os testes.
3. O Render detecta a mudança e faz o deploy automático.
4. O `Dockerfile` configura: `collectstatic` → `migrate` → `createsuperuser_if_none_exists` → `gunicorn`.

### Armazenamento
- **Estáticos (CSS/JS)**: WhiteNoise (servidos pelo próprio container)
- **Uploads (mídia)**: Cloudinary (persistência externa — o filesystem do Render é efêmero)

## 8. Solução de Problemas Comuns

### Erro: `ModuleNotFoundError` no Host
**Sintoma:** Ao rodar `python manage.py ...` localmente, aparece erro de módulo não encontrado.
**Solução:** Você está rodando no ambiente errado. Use `docker compose exec web`.

### Erro de Renderização de Template
**Sintoma:** `TemplateSyntaxError` ou variáveis não renderizando.
**Solução:**
1. Verifique a sintaxe do template (`{% %}`, `{{ }}`).
2. Certifique-se de que tags não estão quebradas em múltiplas linhas.
3. Rode o teste de renderização:
   ```bash
   docker compose exec web python manage.py test contracts.tests.test_pdf_generation
   ```

### Container não sobe / erro de porta
**Sintoma:** Porta 8000 já em uso.
**Solução:**
```bash
docker compose down
docker compose up -d
```

### Migrações fora de sincronia
**Sintoma:** Erros de `column does not exist` ou tabelas faltando.
**Solução:**
```bash
docker compose exec web python manage.py migrate
```
