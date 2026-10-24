# Map: QR Code na Modal de Sucesso do Inkbin

## Destination

Inclusão de um componente visual de QR Code na modal de sucesso ("Paste created successfully!") em `editor.html` para permitir leitura e acesso imediato via smartphones, em conformidade com o INK Design System v2, internacionalização (`en`, `pt-br`, `cn`) e acessibilidade WCAG 2.1 AA.

## Notes

- **Domínio**: Inkbin — UI Editorial Monocromática e Acessibilidade (`docs/agents/INK_Design_System_v2.md`).
- **Modo de execução**: *Execution carried into the map* — governança e implementação dos tickets diretamente no código fonte, templates Jinja2 e arquivos de tradução.
- **Biblioteca de QR Code**: QRCode.js (`qrcode.min.js`), biblioteca leve e sem dependências vendoreada localmente em `src/inkbin/static/js/qrcode.min.js`.
- **Design System & Estilo**: INK Design System v2 — estética estritamente monocromática, alto contraste com fundo branco `#ffffff` na moldura do código para assegurar a zona de respiro (*quiet zone*), dimensões compactas (~144×144px).
- **Acessibilidade**: WCAG 2.1 AA obrigatório (`role="img"`, `aria-label` localizado nos 3 idiomas).
- **Skills relevantes**: `codebase-design`, `domain-modeling`, `tdd`.

## Decisions so far

- **01 Vendor QRCode.js e Estilos INK**: Vendoreamento local de `qrcode.min.js` e estilização de `.modal-qr-section`, `.modal-qr-container`, `.qr-code-box` e `.qr-hint-text` em `ink-editorial.css`. ([01-vendor-qrcode-and-styles.md](issues/01-vendor-qrcode-and-styles.md))
- **02 Estrutura da Modal e Script do Editor**: Inserção do bloco de QR Code no template `editor.html` e lógica de renderização dinâmica no `showSuccessModal` em `ink-editor.js`. ([02-editor-modal-and-script.md](issues/02-editor-modal-and-script.md))
- **03 Internacionalização e Acessibilidade**: Cadastro de traduções em `en.json`, `pt-br.json` e `cn.json` para os novos elementos da modal. ([03-i18n-and-a11y.md](issues/03-i18n-and-a11y.md))
- **04 Validação e Sincronização do Grafo**: Verificação de integridade, testes de unidade e sincronização do grafo de conhecimento via `graphify update .`. ([04-verification-and-graph-sync.md](issues/04-verification-and-graph-sync.md))

## Not yet specified

- **QR Code no Visualizador (Viewer)**: Avaliar inclusão de ação de compartilhamento com modal/popover de QR Code diretamente na barra de ferramentas do leitor `viewer.html`.
- **Download do QR Code como Imagem**: Avaliar botão opcional para download direto do arquivo PNG/SVG do QR Code caso solicitado pelos usuários.

## Out of scope

- Cores cromáticas ou personalizações estilizadas no QR Code (a identidade é estritamente monocromática baseada no INK Design System).
- Geração de QR Code no backend Python através de novas dependências pesadas (`qrcode`, `pillow`).
- Modificação de endpoints de persistência da API REST ou esquemas de banco de dados.
