# 04 - Integração da camada de cache Redis e middleware de rate limiting por IP

Type: task
Status: open
Blocked by: 03

## Question

Como estruturar o cache assíncrono de leitura de pastes (TTL 1h) e o middleware de rate limiting (100 req/min por IP) com Redis assíncrono, mantendo um fallback transparente em memória para desenvolvimento e testes locais?

## Context & Requirements

- Cache de leitura (RNF001):
  - Chave Redis `paste:{slug}` armazenando payload serializado com expiração de 3600 segundos.
  - Invalidação ou bypass imediato em caso de deleção.
- Rate Limiting (RNF004):
  - Middleware FastAPI inspecionando IP do cliente (considerando cabeçalhos de proxy como `X-Forwarded-For`).
  - Limite de 100 requisições por minuto por IP com resposta `429 Too Many Requests` e cabeçalhos `Retry-After`.
- Arquitetura de fallback:
  - Driver unificado: se a conexão Redis falhar ou a variável `REDIS_URL` não for fornecida, utiliza fallback in-memory (LRU cache / dict de contadores) sem quebrar o servidor.
