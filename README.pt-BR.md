<div align="center">
  🌐 <b>Languages / Idiomas / 语言</b>:
  <a href="README.md">English</a> •
  <a href="README.pt-BR.md">Português (Brasil)</a> •
  <a href="README.zh-CN.md">简体中文</a>
</div>

<br>

<div align="center">

# `>_` INKBIN
### Editorial Pastebin & Anonymous Ephemeral Text Sharing

Plataforma open-source de alto desempenho e segura para publicação e compartilhamento anônimo de textos e trechos de código com URLs curtas e ofuscadas, concebida sob a estética tipográfica do **INK Design System v2** e suporte nativo a internacionalização (i18n).

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-000000?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-000000?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL_16_%7C_SQLite-000000?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Cache](https://img.shields.io/badge/Cache-Redis_7_%7C_In--Memory-000000?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Linter](https://img.shields.io/badge/Code_Style-Ruff-000000?style=for-the-badge&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/badge/Docker-Compose_Ready-000000?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-Passed-000000?style=for-the-badge&logo=pytest&logoColor=white)](tests)
[![License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge)](LICENSE)

<br>

[Galeria Visual](#-galeria-visual-e-demonstração) •
[Recursos](#-recursos-principais) •
[Início Rápido](#-início-rápido) •
[Variáveis de Ambiente](#-variáveis-de-ambiente) •
[Uso via Terminal (cURL)](#-guia-de-uso-via-terminal-curl) •
[API REST](#-referência-da-api-rest) •
[Arquitetura](#-arquitetura-e-estrutura) •
[Desenvolvimento & Contribuição](#-desenvolvimento-e-contribuição) •
[Licença](#-licença)

</div>

---

## 📸 Galeria Visual e Demonstração

A interface do Inkbin foi construída estritamente sob as diretrizes do **INK Design System v2**, unindo tipografia editorial monocromática de alto contraste, alvos táteis confortáveis, contadores em tempo real, suporte a múltiplos idiomas e ícones vetoriais Tabler Icons.

| Editor View | Viewer View |
| :---: | :---: |
| <img src="docs/assets/screenshots/editor-view.png" alt="Editor View" width="550"> | <img src="docs/assets/screenshots/viewer-view.png" alt="Viewer View" width="550"> |
| *Formulário de criação com suporte a indentação por tecla Tab, detecção de sintaxe, política dinâmica de expiração, senha opcional e contadores dinâmicos de caracteres/bytes.* | *Visualizador de código com cabeçalho de metadados, contagem de visualizações, ações rápidas (Copiar Código, Ver Raw, Excluir, Denunciar) e destaque de sintaxe.* |

| Modal de Confirmação & Admin Delete Token | Desafio de Senha (Security Gate) |
| :---: | :---: |
| <img src="docs/assets/screenshots/admin-delete-modal.png" alt="Admin Delete Modal" width="550"> | <img src="docs/assets/screenshots/password-challenge.png" alt="Password Challenge" width="550"> |
| *Modal pós-criação apresentando a URL pública curta (Slug Base62) e a chave secreta irrecuperável concedida ao autor anônimo para exclusão permanente imediata.* | *Tela de desafio para Protected Pastes, requerendo validação criptográfica (Argon2id) antes de descriptografar e exibir o conteúdo protegido.* |

---

## ⚡ Recursos Principais

- **Anonymous Creation**: Publicação instantânea e simplificada sem exigência de cadastro, conta de usuário, e-mail ou rastreamento de telemetria.
- **Internacionalização Nativa (i18n)**: Suporte completo a múltiplos idiomas (Inglês `en` padrão, Português do Brasil `pt-br` e Chinês Simplificado `cn`) com alternância rápida na interface via seletor monocromático e persistência em cookie seguro.
- **Slugs Base62 Ofuscados**: URLs públicas geradas com identificadores alfanuméricos curtos (6 a 8 caracteres) calculados em Base62 não sequencial, prevenindo ataques de enumeração e scraping automatizado.
- **Políticas de Expiração Dinâmicas (`EXPIRATION_OPTIONS`)**: Prazos de retenção parametrizáveis via variável de ambiente Docker/Compose (ex.: `1h,1d,1w,1m,never` ou minutos `10m,30m`), com parser flexível e purga automática física do banco de dados e do cache.
- **Histórico Local no Navegador**: Gerenciamento de publicações recentes salvas com segurança no `localStorage` do cliente, com botões de exclusão individual (`ti-x`) e limpeza completa imediata sem recarregar a página.
- **Protected Pastes com Criptografia Argon2id**: Bloqueio de visualização por senha armazenada com algoritmo moderno e resistente a ataques de força bruta (Argon2id), com limitação inteligente após 5 tentativas consecutivas incorretas.
- **Admin Delete Token**: Chave de segurança criptográfica única gerada no momento da criação, garantindo ao autor permissão irrevogável para exclusão permanente do Paste a qualquer momento.
- **Anti-Spam & Rate Limiting**: Algoritmo de janela deslizante via Redis com mitigação imediata de spam bursts através de hashing SHA-256 de conteúdo duplicado.
- **Dual-Engine de Dados com Zero-Config**: Suporte nativo e transparente tanto a **PostgreSQL 16** (com driver assíncrono de alto desempenho `asyncpg` para produção) quanto a **SQLite** (`aiosqlite` para desenvolvimento local sem dependências externas).
- **INK Design System v2 & Acessibilidade**: Interface editorial monocromática de alto contraste, alinhada aos padrões WCAG 2.1 AA, fontes sem serifa modernas e ícones Tabler Icons perfeitamente integrados.

---

## 🚀 Início Rápido

### Opção 1: Docker Compose (Recomendado para Produção / Self-Hosting)

Com apenas dois comandos, suba o cluster completo contendo a aplicação FastAPI, o banco PostgreSQL 16 e o cache Redis 7:

```bash
# 1. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 2. Inicialize todos os serviços com build da imagem
docker compose up --build -d
```

A aplicação estará disponível em `http://localhost:8000`.

Para verificar o status de saúde do cluster:

```bash
curl -fsS http://localhost:8000/health
# Saída esperada: {"status":"ok","app":"inkbin"}
```

Para inspecionar os logs em tempo real:

```bash
docker compose logs -f app
```

---

### Opção 2: Desenvolvimento Local (Zero-Config com SQLite)

Caso você queira rodar localmente sem precisar instalar Docker, PostgreSQL ou Redis, o Inkbin possui mecanismo de fallback automático: ao omitir `REDIS_URL` ou configurar `DATABASE_URL` para SQLite, a aplicação opera transparentemente em memória e com banco local `inkbin.db`:

```bash
# 1. Crie e ative o ambiente virtual Python 3.11+
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 2. Instale o pacote em modo editável com as dependências de desenvolvimento
pip install -e ".[dev]"

# 3. Inicialize o servidor de desenvolvimento com hot-reload
uvicorn inkbin.main:app --reload --port 8000
```

Abra seu navegador em [http://localhost:8000](http://localhost:8000).

---

## ⚙️ Variáveis de Ambiente

As configurações do Inkbin são gerenciadas centralizadamente via Pydantic `BaseSettings` no arquivo `.env`. Veja a referência completa das opções disponíveis:

| Variável | Tipo | Padrão | Descrição |
| :--- | :---: | :---: | :--- |
| `APP_ENV` | `string` | `development` | Ambiente de execução (`development`, `production`, `test`). |
| `DEBUG` | `boolean` | `true` | Habilita modo de depuração e tracebacks informativos. |
| `SECRET_KEY` | `string` | `insecure-dev-...` | Chave secreta de alta entropia (32+ caracteres) para assinatura de tokens de desbloqueio de Pastes. |
| `HOST` | `string` | `0.0.0.0` | Endereço IP de escuta do servidor web. |
| `PORT` | `integer` | `8000` | Porta TCP do serviço web HTTP. |
| `BASE_URL` | `string` | `http://localhost:8000` | URL canônica usada para gerar os links públicos de compartilhamento nos modais e na API. |
| `DATABASE_URL` | `string` | `sqlite+aiosqlite:///./inkbin.db` | String de conexão SQLAlchemy Asyncio (`postgresql+asyncpg://...` ou `sqlite+aiosqlite:///...`). |
| `REDIS_URL` | `string \| null` | `null` | URL do Redis para cache L2 e rate limit (`redis://redis:6379/0`). Se omitido, opera com cache e rate limit em memória. |
| `RATE_LIMIT_PER_MINUTE` | `integer` | `100` | Taxa máxima de requisições por minuto por endereço IP cliente. |
| `MAX_PASTE_BYTES` | `integer` | `1048576` *(1 MB)* | Tamanho máximo permitido em bytes para o corpo de um Paste. |
| `EXPIRATION_OPTIONS` | `string` | `1h,1d,1w,1m,never` | Lista de opções de expiração permitidas na API e no formulário. Suporta minutos (`10m`), horas (`1h`), dias (`1d`), semanas (`1w`), meses (`1m`) e permanente (`never`). |

---

## 💻 Guia de Uso via Terminal (cURL)

O Inkbin foi projetado para interoperabilidade completa via terminal e linha de comando:

### 1. Criar um Paste Anônimo Simples

```bash
curl -X POST http://localhost:8000/api/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "deploy.sh",
    "content": "docker compose up -d",
    "language": "bash",
    "expiration": "1w"
  }'
```

**Resposta:**
```json
{
  "slug": "a8K9x2",
  "url": "http://localhost:8000/p/a8K9x2",
  "admin_delete_token": "del_9f81a7b3c2e104d88e40f5a77b2",
  "title": "deploy.sh",
  "language": "bash",
  "expires_at": "2026-10-30T17:30:00Z",
  "created_at": "2026-10-23T17:30:00Z",
  "is_protected": false
}
```

### 2. Publicar um Arquivo Local Diretamente

```bash
# Usando python para empacotar o arquivo com segurança em JSON:
python3 -c "import json, sys; print(json.dumps({'title': 'main.py', 'language': 'python', 'content': sys.stdin.read()}))" < main.py | \
  curl -s -X POST http://localhost:8000/api/pastes \
    -H "Content-Type: application/json" \
    -d @-
```

### 3. Criar um Protected Paste Protegido por Senha

```bash
curl -X POST http://localhost:8000/api/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Credenciais Confidenciais",
    "content": "API_KEY=ink_sec_9941a87b\nDB_PASS=vault_secret_99",
    "language": "yaml",
    "expiration": "1d",
    "password": "MinhaSenhaForte123"
  }'
```

### 4. Obter Conteúdo Bruto em Texto Puro (Raw Text)

Ideal para scripts de automação, `curl | bash` ou download direto:

```bash
curl -s http://localhost:8000/raw/a8K9x2
# ou pela rota de API:
curl -s http://localhost:8000/api/pastes/a8K9x2/raw
```

### 5. Excluir um Paste com o Admin Delete Token

O autor anônimo pode destruir seu Paste a qualquer momento enviando o token gerado na criação no cabeçalho `X-Admin-Delete-Token`:

```bash
curl -X DELETE http://localhost:8000/api/pastes/a8K9x2 \
  -H "X-Admin-Delete-Token: del_9f81a7b3c2e104d88e40f5a77b2"
```

---

## 🔌 Referência da API REST

Todas as respostas de dados são serializadas em JSON sob codificação UTF-8.

| Método | Endpoint | Cabeçalhos / Parâmetros | Descrição | Códigos de Retorno |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/pastes` | `Content-Type: application/json` | Cria um novo Paste (anônimo ou protegido por senha). | `201 Created`, `400 Bad Request`, `413 Payload Too Large`, `422 Unprocessable Entity`, `429 Too Many Requests` |
| `GET` | `/api/pastes/{slug}` | — | Retorna metadados e conteúdo do Paste em formato JSON. | `200 OK`, `401 Unauthorized` *(requer senha)*, `404 Not Found`, `451 Unavailable For Legal Reasons` |
| `GET` | `/api/pastes/{slug}/raw` | — | Retorna o conteúdo bruto do Paste em texto puro (`text/plain`). | `200 OK`, `401 Unauthorized`, `404 Not Found`, `451 Unavailable For Legal Reasons` |
| `GET` | `/raw/{slug}` | — | Rota curta canônica para download e leitura do texto bruto em texto puro. | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `POST` | `/api/pastes/{slug}/unlock` | `Content-Type: application/json` | Valida senha de Protected Paste e emite cookie seguro de desbloqueio. | `200 OK`, `401 Unauthorized`, `404 Not Found`, `429 Too Many Requests` *(após 5 erros)* |
| `DELETE`| `/api/pastes/{slug}` | `X-Admin-Delete-Token: <token>` | Exclui fisicamente o Paste do banco de dados e invalida os caches. | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `POST` | `/api/pastes/{slug}/report` | `Content-Type: application/json` | Envia denúncia de moderação (`spam`, `malware`, `leak`, `abuse`, `other`). | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `PATCH`| `/api/pastes/{slug}/deactivate`| — | Desativação administrativa de Paste infrator por moderação. | `200 OK`, `404 Not Found` |
| `GET` | `/set-locale/{locale}` | — | Altera o idioma ativo da interface (`en`, `pt-br`, `cn`) e grava cookie `inkbin_locale`. | `303 See Other` |
| `GET` | `/health` | — | Healthcheck de integridade do serviço. | `200 OK` |

---

## 🏗️ Arquitetura e Estrutura

O Inkbin foi projetado com arquitetura assíncrona moderna, isolamento de camadas e separação clara entre regras de domínio, adaptadores de banco de dados e interfaces de apresentação:

```
TextEditor/
├── src/
│   └── inkbin/
│       ├── config.py           # Configuração centralizada Pydantic BaseSettings
│       ├── db.py               # SQLAlchemy 2 Asyncio e migração incremental de esquema
│       ├── expiration.py       # Parser dinâmico de durações e expiração configurável
│       ├── i18n.py             # Módulo de localização, resolução em cascata e helper t()
│       ├── locales/            # Catálogos de tradução estruturados (en.json, pt-br.json, cn.json)
│       ├── models.py           # Modelos ORM relacionais (Paste, PasteReport)
│       ├── schemas.py          # Schemas Pydantic para validação e serialização da API
│       ├── services.py         # Regras de negócio, inserções e queries de banco de dados
│       ├── slug.py             # Gerador de identificadores únicos Base62 (6-8 caracteres)
│       ├── security.py         # Criptografia Argon2id, tokens de exclusão e desbloqueio
│       ├── rate_limit.py       # Middleware assíncrono de taxa de requisição e anti-spam
│       ├── cache.py            # Cache de dois níveis (L1 Memória / L2 Redis)
│       ├── lifecycle.py        # Rotinas de expiração e purga de dados
│       ├── main.py             # Instância do FastAPI, lifespan e rotas principais
│       ├── routes/
│       │   ├── api.py          # Endpoints REST e serialização de respostas
│       │   └── web.py          # Renderização de templates Jinja2 e páginas do usuário
│       ├── static/             # Tokens INK Design System (CSS), JS e fontes
│       └── templates/          # Templates Jinja2 semânticos com Tabler Icons e i18n
├── tests/                      # Suíte de testes automatizados com pytest
├── docs/                       # Especificações de design, documentação técnica e assets
│   ├── adr/                    # Architecture Decision Records
│   ├── agents/                 # Manuais e diretrizes do ecossistema de agentes
│   └── assets/screenshots/     # Capturas de tela em alta resolução da interface
├── docker-compose.yml          # Definição multi-serviço (App, PostgreSQL 16, Redis 7)
├── Dockerfile                  # Imagem Docker multi-stage minimalista
├── pyproject.toml              # Metadados do projeto, dependências e configurações Ruff/pytest
└── GLOSSARY.md                 # Vocabulário canônico do domínio Inkbin
```

---

## 🤝 Desenvolvimento e Contribuição

Contribuições da comunidade são muito bem-vindas! Siga as diretrizes abaixo para colaborar com o projeto:

### 1. Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/gugaucb/inkbin.git
cd inkbin

# Crie um branch dedicado para sua funcionalidade ou correção
git checkout -b feat/minha-melhoria

# Configure o ambiente virtual e dependências
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Execução da Suíte de Testes Automatizados

O projeto mantém rigorosa cobertura de testes de integração, rotas de API, segurança, internacionalização e interface gráfica:

```bash
pytest
```

### 3. Validação de Estilo e Formatação

Utilizamos o [Ruff](https://github.com/astral-sh/ruff) para garantir qualidade e consistência no código Python:

```bash
# Verificação de linting
ruff check .

# Verificação de formatação
ruff format --check .

# Aplicar formatação automática se necessário
ruff format .
```

---

## 📄 Licença

Este projeto é software livre e open-source distribuído sob os termos da licença [MIT](LICENSE).

<div align="center">
  <sub>Desenvolvido com foco em privacidade, simplicidade e precisão editorial.</sub>
</div>
