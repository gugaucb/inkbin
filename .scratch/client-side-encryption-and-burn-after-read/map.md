# Map: Criptografia Client-side, Burn After Read e Codificação Base64

## Destination

Implementação das funcionalidades de segurança avançada e formatos de privacidade no Inkbin: Criptografia ponta-a-ponta no navegador com AES-256-GCM (com chave no fragmento `#key` e nunca enviada ao servidor), Destruição após leitura (*Burn after read*) com tela intermediária de confirmação para prevenir consumo indevido por robôs/crawlers, e Codificação Base64 com aviso editorial de transparência e alternância no visualizador, em total aderência ao INK Design System v2 e suporte i18n (`en`, `pt-br`, `cn`) conforme `.scratch/client-side-encryption-and-burn-after-read/spec.md`.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática, Privacidade Sem Rastreadores e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — o esforço define decisões, contratos de dados, migração de esquema, lógica criptográfica cliente (Web Crypto API), ciclo de vida do descarte e templates editoriais.
- **Modelo de Domínio Atualizado**: Nomes canônicos em `GLOSSARY.md` (`Client-Side Encryption`, `Burn After Read`, `Base64 Encoding`).
- **Design System & Acessibilidade**: Monocromático, fontes Inter/JetBrains Mono, foco e navegação via teclado, suporte para telas pequenas (`<= 639px`).
- **Skills relevantes**: `codebase-design`, `architecture-patterns`, `tdd`, `domain-modeling`.

## Decisions so far

- 01: [01-schema-and-model-migrations.md](issues/01-schema-and-model-migrations.md) — Adicionados campos `content_format` e `burn_after_read` no modelo `Paste`, migração incremental em `_sync_migrate_schema`, esquemas Pydantic e serviços de persistência.

## Not yet specified

- **Integração com Câmera / Escaneamento Direto de QR Code**: Permitir decifrar hashes AES ao escanear QR Code embutido diretamente da webcam no desktop.
- **Contador Regressivo na Tela de Burn After Read**: Exibição de contagem regressiva visual de expiração de sessão caso o leitor permaneça na tela intermediária sem confirmar.
- **Compressão Pré-Cifragem (Deflate / Gzip)**: Avaliar compressão de grandes payloads no navegador antes da cifra AES-256-GCM para reduzir o consumo de tráfego.

## Out of scope

- Criptografia com chave privada assimétrica RSA / PGP de múltiplos destinatários (foge da simplicidade do Inkbin).
- Armazenamento ou decifração no backend da chave contida no fragmento de URL `#key` (viola a garantia de *Zero-Knowledge*).
- Autenticação por conta ou vínculo de identidade de autor/leitor (viola *Anonymous Creation*).
