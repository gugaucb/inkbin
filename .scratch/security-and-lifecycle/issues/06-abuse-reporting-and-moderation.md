# 06: Denúncia Pública de Conteúdo e Desativação Administrativa

**What to build:** Leitores de Pastes contendo conteúdo abusivo, dados vazados ou malware podem submeter uma denúncia fundamentada através de um botão e modal discreto na interface editorial. A denúncia é registrada via API incrementando o contador de denúncias. Moderadores e administradores da plataforma contam com mecanismo de intervenção para desativar o registro (`is_active: false`), tornando-o imediatamente indisponível publicamente (resposta HTTP 451 ou 404).

**Blocked by:** 05: Deduplicação por Hash de Conteúdo e Mitigação de Rajadas de Spam

**Status:** ready-for-agent

- [ ] Botão "Denunciar conteúdo" e modal editorial acessível (WCAG 2.1 AA) na página de visualização de Paste.
- [ ] Endpoint público `POST /api/pastes/{slug}/report` aceitando payload com `reason` (enum com motivos padrão) e `details` (opcional).
- [ ] Incremento atômico de `report_count` no banco de dados e notificação de log de auditoria.
- [ ] Campo booleano `is_active` (padrão `true`) na tabela `pastes`.
- [ ] Endpoint ou script administrativo protegido por token de operador para alternar `is_active = false`.
- [ ] Pastes desativados administrativamente retornam imediatamente status HTTP 451 Unavailable For Legal Reasons (ou 404) tanto na interface web quanto na rota `/raw/{slug}` e evictam o cache Redis.
- [ ] Testes automatizados cobrem envio de denúncia válido, limites de rate-limit para reports pelo mesmo IP e comportamento de bloqueio imediato após desativação.
