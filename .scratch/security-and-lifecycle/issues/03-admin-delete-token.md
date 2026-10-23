# 03: Exclusão Permanente sob Demanda via Admin Delete Token

**What to build:** O criador anônimo de um Paste pode utilizar o `Admin Delete Token` (recebido na resposta de criação) para revogar e excluir permanentemente seu Paste. A interface web apresenta diálogo editorial de confirmação com aviso de irrevogabilidade. A autorização correta remove fisicamente o registro do banco de dados e expurga o cache Redis, fazendo com que qualquer requisição futura retorne HTTP 404.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Geração de token criptograficamente seguro com 64 caracteres (`secrets.token_urlsafe(32)`) retornado unicamente na resposta de criação anônima.
- [ ] Armazenamento no banco apenas do hash SHA-256 do token (`admin_delete_hash`), garantindo segurança em repouso.
- [ ] Endpoint `DELETE /api/pastes/{slug}` aceitando o token no cabeçalho `X-Admin-Delete-Token`.
- [ ] Rota web `GET /{slug}/delete` renderizando página editorial INK com botão de confirmação explícito.
- [ ] Validação rigorosa do hash do token informado; tokens inválidos recebem resposta HTTP 403 Forbidden.
- [ ] Confirmação da exclusão remove permanentemente o registro da tabela `pastes` e evicta a chave correspondente do Redis.
- [ ] Requisições subsequentes ao slug excluído recebem status HTTP 404 Not Found.
- [ ] Testes de integração validam exclusão autorizada, rejeição de tokens incorretos e invalidação instantânea do cache.
