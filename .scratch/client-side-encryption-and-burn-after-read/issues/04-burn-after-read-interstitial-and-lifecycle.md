# 04 - Tela Intermediária e Ciclo de Vida do Burn After Read

Status: resolved
Type: task
Blocked by: 01, 02

## Question

Como implementar a rota de interceptação web (`src/inkbin/routes/web.py`), o template intermediário editorial `burn_confirmation.html` e o ciclo de vida de expurgo definitivo após confirmação do leitor para pastes configurados com *Burn after read*?

## Scope

1. Criar o template `src/inkbin/templates/burn_confirmation.html`:
   - Seguir o design system editorial INK v2: cartão monocromático com bordas limpas, badge com ícone (`ti-flame`), título claro e descrição preventiva.
   - Informações contextuais do paste (título opcional, linguagem de programação, data de publicação).
   - Botão de ação primário para submissão: `[ Revelar e Destruir Paste ]`.
   - Botão secundário para voltar à página inicial.
2. Atualizar a rota web `viewer_page()` em `src/inkbin/routes/web.py`:
   - Se `paste.burn_after_read == True` e a requisição for um simples `GET /p/<slug>` sem confirmação ativa:
     - Renderizar `burn_confirmation.html` com código HTTP 200.
     - **Não incrementar visualizações e não deletar o paste**.
   - Criar rota de confirmação `POST /p/<slug>/reveal` (ou processar com token de ação/confirmação segura):
     - Validar que o paste existe e não expirou.
     - Deletar fisicamente o registro de `Paste` do banco de dados relacional e expurgar do cache (Redis/em-memória).
     - Renderizar o `viewer.html` contendo os dados do paste antes da deleção, acompanhado de banner editorial informando que o documento foi consumido e expurgado permanentemente.
3. Atualizar endpoint da API `GET /api/pastes/{slug}` em `src/inkbin/routes/api.py`:
   - Se `paste.burn_after_read == True`, aceitar parâmetro de confirmação (ex: `confirm_burn=true` ou deletar imediatamente se explicitado na requisição da API) para prevenir consumo por ferramentas automatizadas sem consentimento.
4. Testes de ciclo de vida cobrindo:
   - Acesso inicial a paste com `burn_after_read` retorna a tela intermediária sem alterar o banco.
   - Revelação confirmada entrega o paste e expurga permanentemente.
   - Acesso subsequente ao mesmo slug retorna estritamente 404.

## Answer

Implementado com sucesso o ciclo de vida e tela intermediária para pastes com Burn After Read:
1. Template editorial `burn_confirmation.html` criado em conformidade com o INK Design System v2, exibindo metadados prévios sem revelar o conteúdo, prevenindo que crawlers ou prévias de mensageiros destruam o paste prematuramente. O formulário preserva fragmentos de URL `#key` em submits client-side.
2. Rota `viewer_page()` em `src/inkbin/routes/web.py` atualizada para retornar `burn_confirmation.html` sem incrementar visualizações ou expurgar dados quando `paste.burn_after_read == True`.
3. Rota de confirmação `POST /p/{slug}/reveal` criada para capturar os dados do documento, expurgar permanentemente o registro de `Paste` do banco relacional, invalidar o cache e renderizar `viewer.html` com banner editorial de descarte permanente (`was_burned=True`).
4. Endpoint `GET /api/pastes/{slug}` atualizado para exigir confirmação ativa `confirm_burn=true` antes de entregar o payload e expurgar os dados, retornando HTTP 400 informativo caso omitido.
5. Suíte de testes `tests/test_burn_after_read.py` cobrindo o fluxo completo end-to-end de retenção, expurgo e acesso 404 subsequente aprovada com sucesso.
