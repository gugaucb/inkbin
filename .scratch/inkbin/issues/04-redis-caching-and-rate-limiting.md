# 04 - Integração da camada de cache Redis e middleware de rate limiting por IP

Type: task
Status: resolved
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

## Answer

Camada unificada de cache e rate limiting implementada com driver duplo (Redis + InMemory fallback):
1. `src/inkbin/cache.py`: `CacheService` com suporte a Redis assíncrono (`redis.asyncio`) e fallback automático em memória (`InMemoryCache`) com expiração de TTL. Em `GET /api/pastes/{slug}`, chave `paste:{slug}` é armazenada com TTL de 3600 segundos (ou menor se o paste tiver expiração configurada).
2. `src/inkbin/rate_limit.py`: `RateLimiter` e `RateLimitMiddleware` inspecionando cabeçalhos `X-Forwarded-For` e IP de cliente. Limite configurável (padrão 100 req/min). Ao estourar o limite, responde com HTTP `429 Too Many Requests` e cabeçalho `Retry-After`.
3. Tratamento robusto de exceções (`RedisError`, `OSError`) com logs apropriados, garantindo que testes e ambientes locais funcionem de forma isolada e resiliente.
4. Cobertura de testes em `tests/test_cache_and_rate_limit.py` validando cache hits, expiração de TTL, fallback em memória e bloqueio 429.
