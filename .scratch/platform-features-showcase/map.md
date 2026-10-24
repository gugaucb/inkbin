# Map: Vitrine de Recursos e Garantias da Plataforma

## Destination

Inclusão de uma vitrine informativa monocromática de recursos, privacidade e garantias do Inkbin (Anonymous, Encrypted sharing, Auto-expiry, Developer ready, Privacy focused, Syntax highlighting, No sign-up, Admin Delete Token) diretamente no layout principal (`editor.html`), com suporte completo a i18n (`en`, `pt-br`, `cn`) e otimização ergonômica prioritária para telas menores (`<= 639px`), em conformidade com o INK Design System v2 e `.scratch/platform-features-showcase/spec.md`.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — o esforço define decisões, contratos de tradução i18n, marcação semântica Jinja2 e estilos responsivos em CSS.
- **Prioridade explícita do usuário**: "privilegiar as funcionalidades em telas menores" — densidade compacta, sem empurrar campos essenciais para fora da viewport inicial, alvos de toque adequados e tipografia refinada.
- **Alinhamento com o Glossário**: Preservar termos canônicos de `GLOSSARY.md` (Anonymous Creation, Admin Delete Token, Expiration Policy, Protected Paste).
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`, `domain-modeling`.

## Decisions so far

- **[01 - Catálogos i18n para Recursos e Garantias da Plataforma](issues/01-i18n-catalogs-features-and-guarantees.md)**: Adicionada a seção `features` com 8 pilares nos catálogos `en.json`, `pt-br.json` e `cn.json`, com testes em `test_i18n.py`.

## Not yet specified

- **Criptografia Client-side no Navegador (Web Crypto API)**: Avaliar suporte futuro a cifragem ponta-a-ponta no cliente utilizando fragmento de hash de URL (`#key`) no estilo PrivateBin.
- **Detecção Automática de Sintaxe**: Avaliar integração com detector leve em tempo real via JavaScript no evento de digitação/colagem de código no editor.
- **Modal "Sobre / Segurança e Auditoria"**: Avaliar modal dedicado expansível no rodapé para detalhar o algoritmo Argon2id e as políticas de retenção de banco de dados.

## Out of scope

- Criação de contas de usuário, login social ou autenticação persistente (viola o princípio fundamental de Anonymous Creation).
- Coleta de métricas analíticas, rastreamento por terceiros ou retenção de IPs brutos.
- Alteração no esquema relacional de banco de dados ou migrações SQL.
