# 03: Documentação de Funcionalidades Chave e Arquitetura

**What to build:** Estruturar as seções de "Destaques e Recursos Chave" e "Arquitetura & Design" no README.md, detalhando os diferenciais técnicos e de segurança do Inkbin (Anonymous Creation, Base62 Slugs, Expiration Policies, Argon2 Password Protection, Admin Delete Tokens, INK Design System v2) e a visão dos componentes assíncronos da aplicação.

**Blocked by:** 02: Cabeçalho Editorial, Badges de Status e Galeria Visual

**Status:** resolved

- [x] Redigir a seção "Funcionalidades Principais" destacando os pontos fortes do produto (criação anônima sem cadastro, URLs ofuscadas, segurança criptográfica, expiração automática).
- [x] Incorporar com precisão o vocabulário canônico do domínio definido em `GLOSSARY.md` (evitando termos depreciados como "Snippet", "Paste trancado", "TTL").
- [x] Documentar a arquitetura técnica da aplicação (FastAPI, SQLAlchemy 2 async, motor dual PostgreSQL/SQLite, Redis para rate-limit/cache, templates Jinja2 e Tabler Icons).
- [x] Adicionar diagrama de blocos ou árvore descritiva dos módulos principais do projeto.

## Answer

Adicionadas ao `README.md`:
1. Seção "Recursos Principais" com detalhamento dos pilares de Anonymous Creation, Slugs Base62 Ofuscados, Políticas de Expiração & Lifecycle, Protected Pastes com Argon2id, Admin Delete Tokens, Anti-Spam e Dual-Engine de Dados.
2. Vocabulário 100% canônico e alinhado ao `GLOSSARY.md`.
3. Seção "Arquitetura e Estrutura" com documentação da stack assíncrona e árvore descritiva comentada de todos os módulos e diretórios do repositório.

