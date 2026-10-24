# Spec: QR Code na Modal de Sucesso do Inkbin

## 1. Visão Geral
Apresentação de um QR Code na modal (popup) de confirmação de publicação ("Paste created successfully!") em `editor.html`, permitindo a leitura e abertura rápida do paste em dispositivos móveis (smartphones) via câmera.

A implementação segue os preceitos do **INK Design System v2** (estética editorial monocromática, alto contraste com quiet zone branca para leitura confiável da câmera, tokens padronizados e acessibilidade WCAG 2.1 AA) e as diretrizes de internacionalização nos 3 idiomas suportados (`en`, `pt-br`, `cn`).

## 2. Requisitos Funcionais e Técnicos

### 2.1 Biblioteca de QR Code (RF01)
- Biblioteca JavaScript zero-dependency leve vendoreada localmente em `src/inkbin/static/js/qrcode.min.js` (com base no David Shim / QRCode.js), garantindo funcionamento offline, sem latência e sem sobrecarga no backend Python.
- Inclusão do script no bloco de scripts do template `editor.html`.

### 2.2 Apresentação e Layout na Modal (RF02)
- Inserção de uma seção dedicada de QR Code no corpo da modal de sucesso (`#success-modal`) em `editor.html`, posicionada entre o campo de URL pública e a chave secreta (`Admin Delete Token`).
- Estilização em `ink-editorial.css`:
  - Contêiner centralizado monocromático com fundo sutil (`--surface-subtle`), borda (`--border-default`) e cantos arredondados (`--radius-md`).
  - Moldura de alto contraste (`.qr-code-box`) com fundo branco `#ffffff` para garantir a *quiet zone* indispensável para leitura por câmeras de celular em qualquer tema.
  - Dimensões otimizadas de ~144×144px (QR Code gerado em 128×128px com padding interno).
  - Texto explicativo com ícone Tabler (`ti-device-mobile`) instruindo o usuário a apontar a câmera do celular.

### 2.3 Controlador JavaScript e Resolução de URL (RF03)
- No método `showSuccessModal(data)` em `src/inkbin/static/js/ink-editor.js`:
  - Limpar contêiner `#modal-qrcode` antes da renderização para evitar duplicação em múltiplos envios.
  - Tratar a URL para garantir que dispositivos na rede local consigam acessar o paste caso o host acessado no navegador não seja `localhost` (resolução inteligente da URL pública).
  - Instanciar `new QRCode(...)` com `colorDark: "#0a0a0a"`, `colorLight: "#ffffff"` e nível de correção de erro médio (`QRCode.CorrectLevel.M`).

### 2.4 Internacionalização (RF04)
- Adição das chaves de texto e acessibilidade em `src/inkbin/locales/`:
  - `en.json`:
    - `modal.qr_code_label`: "Mobile Access (QR Code)"
    - `modal.qr_code_hint`: "Scan with your phone's camera to open on mobile"
    - `modal.qr_code_aria`: "QR Code for mobile access to the published paste"
  - `pt-br.json`:
    - `modal.qr_code_label`: "Acesso pelo celular (QR Code)"
    - `modal.qr_code_hint`: "Aponte a câmera do celular para abrir o link"
    - `modal.qr_code_aria`: "Código QR para acesso mobile ao paste publicado"
  - `cn.json`:
    - `modal.qr_code_label`: "手机扫码访问（二维码）"
    - `modal.qr_code_hint`: "使用手机相机扫码即可在移动端打开"
    - `modal.qr_code_aria`: "用于手机访问已发布文本的二维码"

### 2.5 Acessibilidade (WCAG 2.1 AA) (RF05)
- O contêiner do QR Code deve conter `role="img"` e atributo `aria-label` descritivo traduzido dinamicamente.
- Garantir ordem lógica de foco e navegação por teclado na modal.
