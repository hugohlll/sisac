# **Guia de Implantação \- SAC (Hospedagem Gratuita)**

Este documento descreve os passos para realizar o deploy da aplicação utilizando o plano gratuito da **Neon.tech** e **Render.com**.

## **1\. Banco de Dados (Neon.tech)**

O Neon oferece um PostgreSQL Serverless com um generoso plano gratuito.

1. Acesse [Neon.tech](https://neon.tech) e crie uma conta.  
2. Crie um novo projeto chamado sisac.  
3. No Dashboard, copie a **Connection String** (formato: postgres://user:password@ep-host.aws.neon.tech/neondb).  
4. Certifique-se de que a opção Pooling esteja desativada para a string de conexão inicial (ou use a porta 5432 padrão).

## **2\. Preparação do Código (Ajustes Finais)**

Para que o Django funcione corretamente no Render, precisamos garantir que as dependências de produção estejam no requirements.txt.

**Adicione ao seu requirements.txt local:**

gunicorn  
whitenoise  
dj-database-url  
python-dotenv

### **Ajuste no core/settings.py**

Para suportar a URL do banco de dados do Neon e servir arquivos estáticos:

import dj\_database\_url

\# ... (em DATABASES)  
DATABASES \= {  
    'default': dj\_database\_url.config(  
        default=os.environ.get('DATABASE\_URL'),  
        conn\_max\_age=600  
    )  
}

\# ... (em MIDDLEWARE, logo após SecurityMiddleware)  
MIDDLEWARE \= \[  
    'django.middleware.security.SecurityMiddleware',  
    'whitenoise.middleware.WhiteNoiseMiddleware',  \# Adicionar aqui  
    \# ...  
\]

\# ... (Configurações de Static Files)  
STATIC\_ROOT \= BASE\_DIR / "staticfiles"  
STATICFILES\_STORAGE \= "whitenoise.storage.CompressedManifestStaticFilesStorage"

## **3\. Hospedagem da Aplicação (Render.com)**

Utilizaremos o **Web Service** do Render baseado em Docker.

1. Conecte seu repositório do GitHub ao [Render.com](https://render.com).  
2. Crie um novo **Web Service**.  
3. Selecione o repositório sisac.  
4. **Configurações Importantes:**  
   * **Runtime:** Docker.  
   * **Plan:** Free.  
5. **Variáveis de Ambiente (Advanced \-\> Add Environment Variable):**  
   * DATABASE\_URL: A string de conexão que você copiou do Neon.  
   * DJANGO\_SECRET\_KEY: Uma chave aleatória (não use a de desenvolvimento).  
   * DEBUG: False.  
   * DJANGO\_ALLOWED\_HOSTS: .onrender.com (ou o domínio que o Render te der).

## **4\. Pipeline de CI/CD**

O arquivo .github/workflows/ci.yml que você já possui garantirá que o deploy só seja seguro. No Render, você pode configurar o **Auto Deploy** para No e usar o **Deploy Hook** (URL fornecida pelo Render) dentro do seu Workflow do GitHub para que o deploy só ocorra se os testes passarem.

### **Comandos de Build no Render**

Como estamos usando Docker, o Render executará o Dockerfile. Certifique-se de que o CMD final no Dockerfile de produção seja:

CMD \["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:10000"\]

*(O Render geralmente usa a porta 10000 por padrão).*

## **5\. Verificação Pós-Deploy**

Após o build completar:

1. Acesse a URL gerada pelo Render.  
2. Vá para /admin e crie um superusuário (via Render Shell ou comando remoto).  
3. Teste a geração de um contrato para validar se o WeasyPrint está renderizando corretamente com as bibliotecas do sistema instaladas no Docker.

**Nota sobre o Plano Free:** O Render coloca a aplicação para "dormir" após 15 minutos de inatividade. O primeiro acesso após esse período pode levar cerca de 30-50 segundos para despertar.