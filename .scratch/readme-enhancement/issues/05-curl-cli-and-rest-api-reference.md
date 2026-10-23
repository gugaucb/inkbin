# 05: Guia de Uso via Terminal (cURL) e Referência da API REST

**What to build:** Enriquecer o README.md com exemplos interativos de uso diretamente pelo terminal (cURL/CLI) para publicação, recuperação e remoção de pastes sem necessidade de navegador, acompanhado de uma tabela de referência dos endpoints REST disponíveis na aplicação.

**Blocked by:** 02: Cabeçalho Editorial, Badges de Status e Galeria Visual

**Status:** resolved

- [x] Incluir comandos cURL práticos e testados para criação anônima de paste (via payload JSON e upload de arquivo).
- [x] Fornecer exemplos de criação de pastes com senha e tempo de expiração definidos via terminal.
- [x] Documentar o comando para obtenção de conteúdo bruto em texto puro (`GET /api/pastes/{slug}/raw`).
- [x] Demonstrar a exclusão via terminal utilizando o cabeçalho `X-Admin-Delete-Token`.
- [x] Adicionar tabela de referência da API REST contendo métodos HTTP, rotas, finalidade e códigos de resposta esperados.

## Answer

Adicionadas ao `README.md`:
1. Seção "Guia de Uso via Terminal (cURL)" com comandos funcionais e testados para:
   - Criação anônima de Paste via JSON;
   - Publicação de arquivos locais diretamente da linha de comando;
   - Criação de Protected Paste protegido por senha e expiração;
   - Download de conteúdo bruto em texto puro (`/raw/{slug}` e `/api/pastes/{slug}/raw`);
   - Exclusão com cabeçalho `X-Admin-Delete-Token`.
2. Seção "Referência da API REST" contendo tabela exaustiva com métodos HTTP, rotas, cabeçalhos, parâmetros, finalidade e códigos de status esperados.

