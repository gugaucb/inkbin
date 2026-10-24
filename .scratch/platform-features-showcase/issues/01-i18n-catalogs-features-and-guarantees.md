# 01 - Catálogos i18n para Recursos e Garantias da Plataforma

Status: resolved
Type: task
Blocked by: none

## Question

Como estruturar as chaves e textos nos catálogos de internacionalização (`src/inkbin/locales/en.json`, `pt-br.json`, `cn.json`) para cobrir os 8 pilares da plataforma de maneira uniforme, concisa e alinhada ao vocabulário canônico do `GLOSSARY.md`?

## Scope

1. Adicionar seção `features` nos 3 arquivos de tradução (`en.json`, `pt-br.json`, `cn.json`):
   - `features.heading`: Título da seção (ex: "Platform Guarantees & Features" / "Garantias e Recursos da Plataforma" / "平台保障与特性").
   - `features.anonymous`: "Anonymous" / "No account, no raw IPs stored".
   - `features.encryption`: "Encrypted sharing" / "Optional in-browser encryption & Argon2id protection".
   - `features.expiry`: "Auto-expiry" / "Configurable retention from 10 minutes to 1 week".
   - `features.developer`: "Developer ready" / "HTTP API, curl and raw text links".
   - `features.privacy`: "Privacy focused" / "No analytics, zero tracking cookies".
   - `features.syntax`: "Syntax highlighting" / "100+ languages, clean mono formatting".
   - `features.no_signup`: "No sign-up" / "Open and simple, you stay in total control".
   - `features.delete_token`: "Admin Delete Token" / "One-time delete code for instant removal".
2. Assegurar paridade estrutural de 100% entre os arquivos JSON.
3. Validar se a função `t()` do backend carrega todas as novas chaves sem erros.

## Answer

Adicionada a seção `features` nos catálogos `en.json`, `pt-br.json` e `cn.json` com 100% de paridade para os 8 pilares da plataforma (Anonymous Creation, Encrypted Sharing, Auto-expiry, Developer Ready, Privacy Focused, Syntax Highlighting, No Sign-up, Admin Delete Token), cobrindo títulos e descrições semânticas objetivas. Integrado teste automatizado `test_platform_features_showcase_translations` em `tests/test_i18n.py` validando o carregamento dinâmico e ausência de chaves órfãs em todos os locales suportados.
