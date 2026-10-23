# 04: Ciclo de Vida e Auto-Expiração em Dupla Camada

**What to build:** O criador de um Paste pode selecionar uma política de expiração (`1h`, `1d`, `1w`, `1m` ou `never`). Pastes com prazo vencido tornam-se inacessíveis instantaneamente na leitura (*on-demand*, retornando HTTP 404 e disparando expurgo assíncrono). Uma rotina periódica em segundo plano (*scheduled sweep runner*) é executada a cada 10 minutos para purgar do banco e do Redis todos os registros vencidos que não foram acessados.

**Blocked by:** None (can start immediately)

**Status:** closed

- [x] Campo `expiration` na criação mapeado para cálculo preciso de `expires_at` (UTC) baseado no enum (`1h`, `1d`, `1w`, `1m`, `never`).
- [x] Validação *on-demand* em todas as rotas de leitura (`GET /api/pastes/{slug}`, `GET /{slug}`, `GET /raw/{slug}`): se `expires_at < now()`, retorna status HTTP 404 e enfileira exclusão.
- [x] Implementação de runner assíncrono de limpeza (*sweep runner*) executando query otimizada `DELETE FROM pastes WHERE expires_at IS NOT NULL AND expires_at < NOW()`.
- [x] Invalidação e limpeza automática de chaves correspondentes no Redis durante a execução do runner.
- [x] Pastes configurados com `never` (ou nulo) permanecem preservados indefinidamente.
- [x] Testes automatizados cobrem expiração on-demand simulando avanço no tempo, preservação de pastes não expirados e execução completa do runner de purga.
