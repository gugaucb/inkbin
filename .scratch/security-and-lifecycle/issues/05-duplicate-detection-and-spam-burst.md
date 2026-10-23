# 05: Deduplicação por Hash de Conteúdo e Mitigação de Rajadas de Spam

**What to build:** O sistema calcula automaticamente o hash criptográfico SHA-256 do texto de todo Paste submetido. Ao processar novas publicações, o sistema verifica se o mesmo IP enviou conteúdo idêntico em uma janela móvel de 60 segundos; identificada a repetição em rajada, o sistema reaproveita o slug existente ou rejeita a tentativa com HTTP 429, prevenindo injeção massiva de spam e economizando recursos computacionais e de banco.

**Blocked by:** None (can start immediately)

**Status:** closed

- [x] Cálculo determinístico de hash SHA-256 do conteúdo bruto no momento da submissão em `content_hash`.
- [x] Coluna `content_hash` indexada no banco de dados para buscas rápidas.
- [x] Middleware ou serviço de proteção que armazena no Redis a chave `spam_burst:{client_ip}:{content_hash}` com TTL de 60 segundos.
- [x] Detecção de rajadas repetitivas pelo mesmo IP, retornando o slug existente ou resposta `429 Too Many Requests` com aviso informativo.
- [x] Prevenção de duplicação sem quebrar a privacidade nem a experiência do criador legítimo.
- [x] Testes automatizados validam cálculo exato do hash, detecção de envios idênticos em sequência e liberação normal após expiração da janela de 60s.
