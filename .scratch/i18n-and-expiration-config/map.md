# Map: Internacionalização (i18n), Expiração Configurável e Refinamento do Header no Inkbin

## Destination

Implementar a internacionalização completa do Inkbin com suporte a inglês (`en` - padrão), português brasileiro (`pt-br`) e chinês simplificado (`cn`), configuração dinâmica de períodos de expiração via variável de ambiente Docker (`EXPIRATION_OPTIONS`), remoção do subtítulo "EDITORIAL PASTEBIN" do cabeçalho da sidebar, adição de ações de exclusão no "Histórico Local", versões multilíngues da documentação (`README.md`, `README.pt-BR.md`, `README.zh-CN.md`) e 100% de cobertura de testes automatizados.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — este esforço governa as decisões e a implementação direta dos tickets no código fonte, templates Jinja2 e scripts clientes.
- **Idiomas Suportados**: `en` (default), `pt-br`, `cn` (Simplificado / `zh-CN`).
- **Resolução de Idioma**: Cascata `?lang=` -> cookie `inkbin_locale` -> cabeçalho `Accept-Language` -> fallback `en`, preservando URLs curtas e limpas sem prefixos de rota.
- **Formato dos Catálogos**: Catálogos estruturados JSON em `src/inkbin/locales/` (`en.json`, `pt-br.json`, `cn.json`) com helper `t(key)` no Jinja2 e injeção para o JS.
- **Expiração Configurável**: Variável de ambiente `EXPIRATION_OPTIONS` (ex: `1h,1d,1w,1m,never`) no Docker/Settings, parser dinâmico e validação estrita em `src/inkbin/schemas.py`.
- **Histórico Local**: Adição de botão `ti-x` para exclusão individual de pastes no `localStorage` e botão para limpeza completa.
- **Documentação**: `README.md` (canônico em inglês), `README.pt-BR.md` e `README.zh-CN.md` com banner de alternância no topo.
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`, `domain-modeling`.

## Decisions so far

- **Decisão 1 (Header)**: Remoção do subtítulo redundante "Editorial Pastebin" em `src/inkbin/templates/base.html`, mantendo o logotipo e ícone focados e limpos.
- **Decisão 2 (i18n Backend)**: Implementação de catálogo JSON leve em `src/inkbin/locales/` (`en.json`, `pt-br.json`, `cn.json`) com resolução em cascata (`?lang=` -> cookie `inkbin_locale` -> `Accept-Language` -> default `en`), helper `t(key, **kwargs)` exposto aos templates Jinja2 e middleware de cookie. Endpoint de comutação rápida `GET /set-locale/{locale}`.
- **Decisão 3 (Expiração Dinâmica)**: `EXPIRATION_OPTIONS: str = "1h,1d,1w,1m,never"` configurável via variável de ambiente no Docker/Settings. Parser e validador estrito em `src/inkbin/expiration.py` e `src/inkbin/schemas.py` (`ExpirationValue` compatível com Pydantic v2 core schema e `to_datetime()`), retornando HTTP 422 para prazos não habilitados.
- **Decisão 4 (Templates & Switcher)**: Injeção de `lang` dinâmico na tag `<html>`, catalogo do locale atual injetado em `window.__INK_I18N__`, tradução de todos os templates Jinja2 (`base.html`, `editor.html`, `viewer.html`, `delete_confirmation.html`, `password_challenge.html`, `404.html`, `451.html`), renderização dinâmica das opções de expiração e seletor monocromático acessível no rodapé da barra lateral.
- **Decisão 5 (JS & Histórico Local)**: Helper de tradução client-side `t(key, fallback, params)` em `src/inkbin/static/js/ink-editor.js` para contadores e notificações. Ações de exclusão no Histórico Local: botão individual `ti-x` para remoção pontual (`removePasteFromHistory`) e botão de limpeza total com confirmação (`clearLocalHistory`), respeitando o design system editorial INK.
- **Decisão 6 (Documentação Multilíngue)**: Documentação canônica em inglês (`README.md`), português do Brasil (`README.pt-BR.md`) e chinês simplificado (`README.zh-CN.md`), com switcher no cabeçalho e documentação da variável `EXPIRATION_OPTIONS`.
- **Decisão 7 (Testes & Grafo)**: Atualização das asserções de UI para inglês canônico e cobertura de 100% (66/66 testes passando no pytest). Grafo de conhecimento atualizado com Graphify.


## Not yet specified

- **Tradução de Termos Técnicos Especiais de Sintaxe**: Avaliar no futuro se nomes de linguagens de programação no dropdown (ex: Plaintext, Python, Shell) demandam localização ou devem permanecer no padrão técnico internacional.
- **Auto-detecção Geográfica por IP**: Caso seja requerida no futuro a definição de idioma por geolocalização IP sem depender apenas do `Accept-Language` do browser.

## Out of scope

- Prefixos de rota para idioma (ex: `/pt-br/p/{slug}`) que fragmentariam e poluiriam os slugs curtos e ofuscados.
- Compilação pesada de binários GNU gettext (`.po`/`.mo`) com dependências externas em C.
- Cores cromáticas no seletor de idiomas ou nos botões de exclusão do histórico (manter rigor monocromático INK Design System v2).
