Status: closed

# Especificação: Segurança, Ciclo de Vida e Moderação (Fases 2 e 3)

## Problem Statement

Desenvolvedores, engenheiros de infraestrutura e equipes de TI que utilizam o **Inkbin** para compartilhar logs, trechos de configuração ou códigos confidenciais enfrentam riscos de vazamento quando os dados ficam acessíveis publicamente por URL sem autenticação adicional. Além disso:
- Pastes sem expiração acumulam dados obsoletos indefinidamente, aumentando a superfície de ataque e o custo de armazenamento.
- Criadores anônimos não possuem mecanismo para revogar ou excluir um **Paste** após a publicação sem depender de suporte humano.
- Plataformas públicas abertas à criação anônima sofrem com ataques de força bruta, spam automatizado e publicação de conteúdos abusivos ou maliciosos.

## Solution

O **Inkbin** implementará um modelo integrado de segurança, governança de ciclo de vida e moderação de conteúdo, composto por três pilares essenciais:

1. **Proteção por Senha (Protected Paste)**:
   - Criptografia unidirecional de senhas com **Argon2id** (ou bcrypt cost 12 como alternativa).
   - Bloqueio rigoroso contra força bruta: máximo de 5 tentativas incorretas por IP/Slug, resultando em bloqueio temporário de 15 minutos.
   - Emissão de cookie de sessão assinado com validade de 24 horas após validação bem-sucedida.
   - Imutabilidade absoluta: **Pastes** protegidos não podem ser editados após a criação.

2. **Gerenciamento e Ciclo de Vida**:
   - Exclusão sob demanda pelo criador anônimo mediante apresentação do **Admin Delete Token** gerado exclusivamente no ato da criação.
   - Auto-expiração confiável conforme a **Expiration Policy** configurada (`1h`, `1d`, `1w`, `1m`, `never`), executada por verificação imediata (*on-demand*) e varredura periódica em segundo plano (*background cleanup runner*).

3. **Moderação de Conteúdo e Detecção de Abuso**:
   - Geração de hash criptográfico do conteúdo (SHA-256) para identificar envios duplicados e rajadas de spam.
   - Endpoint de denúncia pública (*report*) para sinalização de conteúdo inadequado.
   - Capacidade administrativa de desativação imediata de pastes sinalizados.

---

## User Stories

1. Como criador anônimo de um **Paste**, quero definir uma senha de acesso (entre 4 e 50 caracteres) no momento da publicação, para que apenas pessoas com a credencial possam visualizar o conteúdo.
2. Como leitor acessando a URL de um **Protected Paste**, quero visualizar uma tela limpa e editorial solicitando a senha, para que eu possa desbloquear o conteúdo de forma intuitiva.
3. Como leitor que inseriu a senha correta de um **Protected Paste**, quero receber uma sessão válida por 24 horas, para que eu não precise digitar a senha a cada recarregamento da página.
4. Como leitor que inseriu uma senha incorreta, quero ver uma mensagem de erro clara informando quantas tentativas ainda restam antes do bloqueio, para que eu não seja bloqueado por engano de digitação.
5. Como sistema, quero bloquear o acesso de um IP à URL de um **Protected Paste** por 15 minutos após 5 tentativas de senha incorretas, para mitigar ataques automatizados de força bruta e enumeração.
6. Como criador de um **Protected Paste**, quero garantia de que o conteúdo jamais poderá ser alterado por terceiros após a criação, para preservar a integridade estrita do registro publicado.
7. Como criador anônimo de um **Paste**, quero receber um **Admin Delete Token** secreto na resposta da criação, para que eu possa excluir permanentemente o paste quando ele não for mais necessário.
8. Como criador anônimo, quero acessar a rota de exclusão com meu **Admin Delete Token**, para confirmar e executar a remoção definitiva do meu **Paste**.
9. Como criador anônimo na tela de exclusão, quero ver um pedido explícito de confirmação antes da destruição dos dados, para evitar exclusões acidentais.
10. Como leitor tentando acessar um **Paste** que já foi excluído via **Admin Delete Token**, quero receber um status HTTP 404 claro com indicação editorial de que o registro não está mais disponível.
11. Como criador de um **Paste**, quero selecionar uma **Expiration Policy** (`1 hora`, `1 dia`, `1 semana`, `1 mês` ou `nunca`), para que os dados sensíveis sejam descartados automaticamente quando perderem a utilidade.
12. Como leitor tentando acessar a URL de um **Paste** cujo prazo de expiração já foi atingido, quero que o sistema recuse a exibição e retorne 404, mesmo antes da execução da rotina agendada de limpeza.
13. Como operador da plataforma, quero que uma rotina em segundo plano purgue do banco de dados e do cache Redis todos os **Pastes** com data de expiração vencida, para manter a base de dados enxuta e otimizada.
14. Como leitor de um **Paste** público contendo código malicioso ou dados vazados, quero clicar em um botão de denúncia e enviar uma justificativa, para alertar os mantenedores da plataforma.
15. Como sistema, quero calcular o hash SHA-256 do conteúdo de cada **Paste** criado, para rejeitar ou aplicar *rate-limit* severo a rajadas idênticas de spam pelo mesmo IP.
16. Como administrador da plataforma, quero dispor de um comando ou endpoint seguro para desativar imediatamente qualquer **Paste** sinalizado, removendo-o da visualização pública sem corromper a integridade dos índices.
17. Como cliente de API consumindo `/raw/{slug}`, quero que a rota de texto puro também exija autenticação por senha (via Basic Auth ou cookie de sessão) caso o **Paste** seja protegido, para não permitir vazamento de conteúdo bruto sem senha.

---

## Implementation Decisions

### 1. Costura de Testes e Fronteira Arquitetural (Testing Seams)
- **Costura Primária (Única e de Mais Alto Nível)**: Fronteira HTTP/ASGI da aplicação FastAPI (`httpx.AsyncClient` executando requisições assíncronas reais contra o app). Nenhum mock interno de serviços de domínio; validação ponta a ponta dos status HTTP, cookies emitidos (`Set-Cookie`), cabeçalhos de segurança, payloads JSON e templates HTML renderizados.
- **Costura Secundária (Rotina Assíncrona)**: Invocação direta da função de varredura periódica de expurgo (*cleanup runner*) em suíte de testes assíncronos, simulando avanço de tempo no banco de dados.

### 2. Módulo de Proteção por Senha (`inkbin.security`)
- **Algoritmo de Hash**: `Argon2id` utilizando a biblioteca `argon2-cffi` (com memória e iterações recomendadas pela OWASP). Opcionalmente compatível com `bcrypt` (fator de custo 12).
- **Esquema de Dados**:
  - `is_protected`: Booleano indicando se o paste exige validação de senha.
  - `password_hash`: String contendo o hash criptográfico (nulo para pastes públicos).
- **Proteção contra Brute Force**:
  - Armazenamento de tentativas no Redis com chave `auth_attempts:{slug}:{client_ip}` (TTL de 900 segundos).
  - Contador incremental atômico (`INCR`). Se `contador >= 5`, qualquer tentativa adicional recebe HTTP 429 com mensagem de bloqueio e tempo restante.
- **Sessão do Leitor**:
  - Cookie assinado criptograficamente `inkbin_unlocked_{slug}` gerado com token HMAC (chave secreta da aplicação).
  - Atributos do cookie: `HttpOnly`, `SameSite=Lax`, `Secure` (em produção), com validade máxima de 24 horas.
  - Acesso à rota web ou `/raw/{slug}` verifica a presença e integridade do cookie para liberar a visualização.

### 3. Módulo de Gerenciamento e Exclusão (`inkbin.lifecycle`)
- **Token de Administração**:
  - Gerado no momento da criação através de `secrets.token_urlsafe(32)` (64 caracteres de alta entropia).
  - O banco de dados armazena apenas o hash SHA-256 do token em `admin_delete_hash` (garantindo que vazamento do banco não permita exclusão de pastes).
- **Endpoint de Exclusão**:
  - `DELETE /api/pastes/{slug}` com cabeçalho `X-Admin-Delete-Token` ou formulário POST `/{slug}/delete` com campo `token`.
  - Se o hash do token coincidir, o paste é removido fisicamente (*hard delete*) do PostgreSQL e sua chave é evictada do cache Redis.
  - Exclusão confirmada via tela web editorial no estilo INK com botão de confirmação irrevogável.

### 4. Mecanismo de Expiração em Dupla Camada
- **Camada 1 — On-Demand**: Toda leitura (`GET /api/pastes/{slug}` e `GET /{slug}`) avalia se `expires_at is not None and expires_at < now()`. Se expirado, a resposta é imediatamente 404 e uma tarefa em background exclui o registro.
- **Camada 2 — Scheduled Sweep Runner**: Tarefa assíncrona periódica (executada a cada 10 minutos via scheduler interno ou cron job externo) que executa `DELETE FROM pastes WHERE expires_at IS NOT NULL AND expires_at < NOW()`.

### 5. Moderação e Anti-Spam (`inkbin.moderation`)
- **Deduplicação e Detecção de Rajadas**: Coluna indexada `content_hash` (SHA-256 do texto). O middleware de criação avalia se o mesmo IP enviou o mesmo hash em um intervalo inferior a 60 segundos, retornando o slug existente ou rejeitando repetições de spam.
- **Denúncia Pública**: Endpoint `POST /api/pastes/{slug}/report` com campos `reason` e `details`. Incrementa `report_count` e adiciona à fila de moderação.
- **Desativação**: Flag `is_active: bool` (padrão `True`). Se desativado administrativamente, o paste retorna HTTP 451 (*Unavailable For Legal Reasons*) ou HTTP 404.

---

## Testing Decisions

- **Filosofia de Testes**: Testar exclusivamente o comportamento observável externamente através das rotas da API e respostas web, evitando testes acoplados à implementação interna de classes ou DAOs.
- **Casos de Teste Essenciais**:
  1. *Criação com Senha*: Submissão de paste com senha válida retorna metadados com `is_protected: true` e não vaza a senha nem seu hash.
  2. *Bloqueio de Leitura sem Senha*: Acesso a paste protegido sem cookie retorna tela de login ou 401/403 na API.
  3. *Validação e Sessão*: Envio da senha correta emite cookie `inkbin_unlocked_{slug}` e libera acesso imediato.
  4. *Rate Limiting / Lockout*: 5 senhas erradas consecutivas bloqueiam o IP para aquele slug por 15 minutos (resposta HTTP 429).
  5. *Exclusão com Token Válido*: Envio do `Admin Delete Token` correto exclui o paste; requisições subsequentes retornam 404.
  6. *Exclusão com Token Inválido*: Envio de token incorreto retorna 403 e mantém o paste intacto.
  7. *Expiração On-Demand*: Paste com expiração simulada no passado retorna 404 imediatamente na tentativa de leitura.
  8. *Varredura de Expiração*: Execução do runner remove pastes vencidos do banco e invalida entradas no Redis.
  9. *Denúncia de Abuso*: Endpoint de report aceita denúncia e atualiza métricas de moderação.

---

## Out of Scope

- Cadastro formal de usuários, tela de registro, recuperação de senha por e-mail ou perfis de usuário (a criação permanece estritamente anônima).
- Edição do conteúdo de pastes já criados (todos os pastes permanecem permanentemente imutáveis).
- Criptografia de ponta a ponta client-side (com derivação de chave e decodificação via WebCrypto no navegador do leitor — reservada para futura especificação de cifra de zero-knowledge).
- Painel SaaS complexo com múltiplos níveis de permissão de moderadores.

---

## Further Notes

- Esta especificação complementa o [INK Design System v2](file:///Users/gustavoluiscosta/Downloads/projetos/TextEditor/docs/agents/INK_Design_System_v2.md). As telas de solicitação de senha, de confirmação de exclusão e de denúncia devem respeitar a paleta monocromática estrita (`--ink-0` a `--ink-950`) e os princípios de acessibilidade WCAG 2.1 AA documentados.
- As migrações de banco de dados no Alembic devem prever as colunas `password_hash`, `is_protected`, `admin_delete_hash`, `content_hash` e `report_count` desde a fundação da Fase 1, evitando quebras estruturais quando as Fases 2 e 3 forem ativadas.
