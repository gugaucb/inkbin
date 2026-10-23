# Spec: Aprimoramento Open-Source do README.md e Assets Visuais

## 1. Visão Geral

Este documento especifica a transformação do [README.md](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/README.md) do Inkbin em uma documentação padrão ouro para projetos open-source de alto impacto. 

O objetivo é transformar a apresentação inicial do repositório em um hub atrativo, confiável e autoexplicativo para usuários, operadores de infraestrutura/self-hosters e desenvolvedores da comunidade, incorporando screenshots reais em alta definição da aplicação editorial, guias de início rápido (Docker e bare-metal), exemplos interativos de uso via terminal (cURL), especificações de API e diretrizes de contribuição em conformidade com o **INK Design System v2** e o [GLOSSARY.md](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/GLOSSARY.md).

## 2. Requisitos e Seções do README

### 2.1 Identidade Visual, Badges e Hero Section
- Título em destaque com a tipografia e branding editorial: **Inkbin**.
- Badges dinâmicos e estilizados:
  - Linguagem: Python 3.11+
  - Framework: FastAPI
  - Banco de Dados: PostgreSQL 16 & SQLite (Zero-Config)
  - Cache & Rate Limiting: Redis 7
  - Estilo de Código: Ruff
  - Licença: MIT
  - Testes: Pytest (passing)
- Frase de impacto concisa definindo o propósito do Inkbin (plataforma minimalista e segura de compartilhamento anônimo e efêmero com design editorial monocromático).
- Links de navegação rápida (Sumário / Table of Contents) com âncoras para todas as seções.

### 2.2 Galeria Visual e Demonstração da Aplicação
- Screenshots reais capturados da interface gráfica web com o tema dark/monocromático do INK Design System:
  - **Editor View**: Formulário de criação com seleção de linguagem, contadores em tempo real, política de expiração e senha.
  - **Viewer View**: Leitor com numeração de linhas, badge de expiração, contador de visualizações, botão de cópia rápida e ações.
  - **Password Challenge / Security Gate**: Tela elegante de proteção de acesso a pastes confidenciais.
  - **Admin Delete Token Modal / Tela de Exclusão**: Modal e fluxo seguro de destruição permanente concedido ao autor.
- Organização em tabela responsiva ou grid markdown com descrições objetivas.

### 2.3 Recursos Chave (Core Features)
- **Anonymous Creation**: Publicação instantânea sem login ou rastreamento.
- **Slugs Base62 Ofuscados**: Identificadores curtos (6-8 caracteres), não sequenciais e resistentes a enumeração.
- **Políticas de Expiração & Lifecycle**: Expiração automática (1h, 1d, 1w, 1m ou permanente) com rotinas de limpeza.
- **Proteção Criptográfica**: Hashes seguros com Argon2id para proteção por senha e rate limiting inteligente (5 tentativas).
- **Admin Delete Token**: Chave única de exclusão permanente gerada no momento da criação.
- **INK Design System & Tabler Icons**: Interface editorial monocromática de alto contraste sem poluição visual.

### 2.4 Quickstart & Guia de Execução
- **Docker Compose (Recomendado)**:
  - Comando único para subir Postgres, Redis e FastAPI: `docker compose up --build`.
  - Instruções de configuração de portas e verificação em `http://localhost:8000`.
- **Desenvolvimento Local (Zero-Config)**:
  - Execução simplificada usando fallback automático para SQLite quando PostgreSQL não estiver configurado.
  - Comandos: ambiente virtual, instalação de dependências e inicialização com `uvicorn`.
- **Tabela de Variáveis de Ambiente**:
  - Detalhamento de cada parâmetro de `.env.example` (`APP_ENV`, `DATABASE_URL`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, `MAX_PASTE_BYTES`, `BASE_URL`).

### 2.5 Guia de Uso via Terminal (cURL) & Referência de API REST
- Exemplos práticos de uso via terminal (estilo hastebin/0x0):
  - Criar um paste via cURL enviando arquivo ou stdin: `curl -X POST -F "content=@meu_arquivo.py" http://localhost:8000/api/pastes`.
  - Criar um paste com senha e expiração personalizada.
  - Obter conteúdo bruto de um paste: `curl -s http://localhost:8000/api/pastes/{slug}/raw`.
  - Deletar paste usando o `X-Admin-Delete-Token`.
- Tabela resumo dos endpoints da API REST com métodos, caminhos e códigos de status HTTP.

### 2.6 Arquitetura e Estrutura do Repositório
- Árvore de diretórios estruturada explicando a modularidade da aplicação (`src/inkbin/`, `static/`, `templates/`, `tests/`, `docs/`).
- Breve visão da stack assíncrona (FastAPI + SQLAlchemy Asyncio + aiosqlite/asyncpg + Redis).

### 2.7 Contribuição, Testes e Governança Open-Source
- Guia para novos contribuidores:
  - Fork, branch e setup local.
  - Execução dos testes automatizados: `pytest`.
  - Validação de formatação e linting: `ruff check .` e `ruff format --check .`.
  - Convenções de issues locais em `.scratch/`.
- Política de segurança e reporte de vulnerabilidades.
- Licença MIT e créditos.

## 3. Critérios de Aceite
1. O `README.md` apresenta estrutura profissional, moderna e legível, com badges válidos e tabela de conteúdos funcional.
2. Todas as screenshots referenciadas existem fisicamente no repositório (em `docs/assets/screenshots/`), são de alta qualidade e refletem o estado atual da interface gráfica com Tabler Icons.
3. Os comandos de instalação, Docker, testes e cURL foram verificados e funcionam perfeitamente.
4. A terminologia respeita integralmente o [GLOSSARY.md](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/GLOSSARY.md).
