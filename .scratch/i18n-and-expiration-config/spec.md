# Spec: Internacionalização (i18n), Expiração Configurável e Refinamento do Header

## 1. Visão Geral

Este documento especifica a implementação completa da internacionalização (i18n) no Inkbin com suporte nativo aos idiomas inglês (`en` — padrão canônico), português do Brasil (`pt-br`) e chinês simplificado (`cn`), parametrização dinâmica de períodos de expiração via variável de ambiente Docker (`EXPIRATION_OPTIONS`), remoção do subtítulo "EDITORIAL PASTEBIN" do cabeçalho da sidebar, funcionalidades de exclusão no "Histórico Local", versões multilíngues da documentação oficial (`README.md`, `README.pt-BR.md`, `README.zh-CN.md`) e conformidade com o INK Design System v2 e suíte de testes.

## 2. Requisitos Funcionais

### 2.1 Remoção do Subtítulo 'EDITORIAL PASTEBIN' (RF01)
- Remover o elemento `<div class="brand-subtitle">Editorial Pastebin</div>` do cabeçalho da sidebar (`.sidebar-header`) em `src/inkbin/templates/base.html`.
- Preservar o título canônico da marca `INKBIN` com seu ícone `ti-terminal` mantendo alinhamento monocromático limpo.

### 2.2 Sistema de Internacionalização Backend & Locales (RF02)
- Idiomas suportados: `en` (default), `pt-br`, `cn` (Simplificado / `zh-CN`).
- Catálogos JSON estruturados sob `src/inkbin/locales/`:
  - `en.json` (todas as chaves de interface e mensagens em inglês);
  - `pt-br.json` (todas as chaves em português brasileiro);
  - `cn.json` (todas as chaves em chinês simplificado).
- Módulo `src/inkbin/i18n.py`:
  - Carregamento e cache dos catálogos JSON;
  - Resolução de idioma em cascata:
    1. Parâmetro de query temporário `?lang=en|pt-br|cn` (que grava o cookie);
    2. Cookie persistente `inkbin_locale`;
    3. Cabeçalho HTTP `Accept-Language`;
    4. Fallback padrão `en`.
  - Helper de tradução `t(key, locale=..., **kwargs)` com interpolação de strings e fallback para `en` caso a chave inexista no idioma selecionado.
- Endpoint `GET /set-locale/{locale}` para alternância rápida com gravação do cookie `inkbin_locale` e redirecionamento.
- Preservação estrita de URLs curtas e limpas sem prefixos de idioma nas rotas.

### 2.3 Expiração Configurável via Docker (RF03)
- Definição da variável de ambiente `EXPIRATION_OPTIONS` no Docker/Settings:
  - Padrão: `1h,1d,1w,1m,never`.
  - Documentação atualizada em `.env.example` e `docker-compose.yml`.
- Parser dinâmico de durações flexíveis (`src/inkbin/expiration.py`):
  - Minutos (`m`), Horas (`h`), Dias (`d`), Semanas (`w`), Meses (`M`/`mo`/`m`), Permanente (`never`).
- Validação estrita no payload da API (`PasteCreateRequest` em `src/inkbin/schemas.py`):
  - Aceitar apenas durações habilitadas em `settings.EXPIRATION_OPTIONS`;
  - Rejeitar opções não permitidas com erro HTTP 422;
  - Fallback para `never` (se habilitado) ou a primeira opção configurada quando omitida na criação.
- Renderização dinâmica do elemento `<select id="paste-expiration">` no editor com rótulos traduzidos conforme o idioma ativo.

### 2.4 Internacionalização dos Templates Jinja2 & Seletor de Idioma (RF04)
- Substituição de todas as strings estáticas hardcoded por chamadas `t(key)`:
  - `base.html` (navegação, seções, avisos de rodapé, acessibilidade);
  - `editor.html` (labels com ícones Tabler, contadores, botões, modal de confirmação de criação);
  - `viewer.html` (metadados do paste, contadores, ações de copiar/raw/excluir/denunciar);
  - `delete_confirmation.html`, `password_challenge.html`, `404.html` e `451.html`.
- Seletor de idioma minimalista e monocromático no rodapé da sidebar (`app-sidebar`):
  - Ícone `ti-world` ou `ti-language`;
  - Opções: "English", "Português (BR)", "简体中文 (CN)";
  - Atributo `lang="{{ current_locale }}"` na tag `<html>`.

### 2.5 Internacionalização do JavaScript e Exclusão no Histórico Local (RF05)
- Injeção das chaves de tradução necessárias para o JavaScript cliente (`src/inkbin/static/js/ink-editor.js`).
- Localização de contadores dinâmicos, textos de botões reativos ("Copiado!"), alertas e mensagens de erro assíncronas.
- Funcionalidades de exclusão no "Histórico Local":
  - Botão individual de exclusão com ícone `ti-x` em cada item de paste recente (`aria-label` e `title` traduzidos);
  - Botão "Limpar histórico" / "Clear history" para esvaziamento imediato da lista;
  - Atualização reativa imediata no `localStorage` (`inkbin_history`) e no DOM sem recarregar a página.

### 2.6 Documentação Multilíngue (RF06)
- `README.md` traduzido integralmente para o inglês (`en`) como padrão principal internacional.
- `README.pt-BR.md` completo em português brasileiro com as novas funcionalidades e parâmetros de ambiente.
- `README.zh-CN.md` completo em chinês simplificado (简体中文).
- Barra de navegação rápida entre idiomas inserida no topo de cada um dos três arquivos.

### 2.7 Validação e Testes Automatizados (RF07)
- Atualização das asserções de UI em `tests/test_web_ui.py` para o padrão `en`.
- Testes automatizados para alternância e persistência de locale (`pt-br`, `cn`, `en`).
- Testes para validação e restrição dinâmica de `EXPIRATION_OPTIONS`.
- 100% de sucesso em toda a suíte de testes existente (56 testes) e novos testes.
- Atualização do grafo de conhecimento via `graphify update .`.
