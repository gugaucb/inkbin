# Spec: Responsividade Multiplataforma no Inkbin

## 1. Visão Geral
Adequação e otimização responsiva completa da aplicação editorial Inkbin para diversos formatos de tela e dispositivos (smartphones de 320px–480px, tablets de 640px–1023px, desktops de 1024px–1439px e monitores ultrawide >= 1440px), em estrita conformidade com as diretrizes do **INK Design System v2** (`docs/agents/INK_Design_System_v2.md`).

A iniciativa soluciona diretamente o problema de ergonomia visual onde elementos com altura rígida (como `#paste-content` com `height: 480px;`) e formulários com disposição desktop estendem a página verticalmente, forçando rolagens excessivas para acessar botões de ação críticos como "Publicar Texto".

## 2. Breakpoints e Regras Canônicas (INK v2)

| Faixa | Viewport | Navegação | Margem Conteúdo | Editor & Viewer |
|---|---|---|---|---|
| **Mobile** | <= 639 px | Drawer retrátil com backdrop | 16 px lateral (`--space-4`) | Coluna única, textarea adaptativa com `clamp()`, ações compactas |
| **Tablet** | 640–1023 px | Drawer ou sidebar retraída | 24 px lateral (`--space-6`) | Grade flexível, campos em 2 colunas se couberem |
| **Desktop** | 1024–1439 px | Sidebar fixa (248 px) | 32 px lateral (`--space-8`) | Layout completo, largura máxima 1120 px |
| **Wide** | >= 1440 px | Sidebar fixa (248 px) | 40 px lateral, centro 1120 px | Leitura max 800 px, editor max 1120 px |

## 3. Requisitos Funcionais e Visuais

### 3.1 Container Global e Barra de Navegação (RF01)
- Topbar responsiva: altura de 56px no mobile (`<= 639px`) e 64px em desktop/tablet.
- Padding do container principal (`page-container`): transição suave de `--space-4` (16px) no mobile para `--space-8` (32px) no desktop.
- Prevenção rigorosa de overflow horizontal global (`html, body { overflow-x: hidden; }` ou controle de largura de containers com `max-width: 100%`).
- Suporte a entalhes e áreas seguras em smartphones (`padding-bottom: env(safe-area-inset-bottom, 16px)`).

### 3.2 Editor e Formulário de Criação (RF02)
- `#paste-content` / `.editor-textarea`:
  - Desktop: manter altura padrão generosa (`480px`).
  - Mobile (`max-width: 639px`): altura adaptativa proporcional à viewport utilizando `height: clamp(220px, 36vh, 320px); min-height: 200px; resize: vertical;`.
- Controles de metadados no mobile:
  - Título do paste: largura 100%, sem quebrar placeholders.
  - Seletores de Linguagem e Prazo de Expiração: dispostos em coluna única ou grade de 2 colunas compactas com largura mínima garantida de toque.
  - Campo de senha: total fluidez horizontal.
- Rodapé de publicação:
  - No mobile, manter o botão "Publicar Texto" com alvo de toque pleno (mínimo 44px de altura) e texto descritivo visível.
  - Espaçamento enxuto entre o editor e as ações para evitar rolagem de tela após o preenchimento.

### 3.3 Visualizador de Texto e Código / Viewer (RF03)
- Confinamento da rolagem horizontal:
  - O bloco `<pre><code id="paste-code">` deve ter `overflow-x: auto; -webkit-overflow-scrolling: touch; max-width: 100%; word-break: normal; white-space: pre;`.
  - O layout da página não pode ser empurrado por linhas extensas de código.
- Barra de ações do leitor (`.viewer-actions`):
  - Em telas menores (`<= 768px` e `<= 640px`), botões secundários devem encolher com elegância ou exibir apenas ícone com `aria-label` e `title`, garantindo que ações principais (Copiar código, Novo, Excluir) continuem acessíveis sem quebras desordenadas.
- Metadados: badges de linguagem, data, visualizações e expiração quebrando em linha flexível com espaçamento consistente (`--space-2`).

### 3.4 Modais e Telas Auxiliares (RF04)
- Modais (`modal-dialog`):
  - Largura responsiva fluida: `width: min(92vw, 480px); margin: 0 auto;`.
  - Caixa de QR Code (`.modal-qr-container`): centralizada e ajustada para caber em telas estreitas (320px) sem transbordar.
  - Campo e botão de copiar URL / Token: agrupamento flexível que quebra em coluna caso a largura útil seja menor que 340px.
- Telas de Senha (`password_challenge.html`), Exclusão (`delete_confirmation.html`) e Erros (404, 451):
  - Cards de formulário centralizados com `max-width: 100%` e margens de segurança para evitar cortes laterais em celulares pequenos.

### 3.5 Qualidade e Acessibilidade (RF05)
- Alvos de toque (touch targets) mínimos de 40px–44px em todos os controles interativos no mobile (WCAG 2.2 AA).
- Foco visual evidente (`:focus-visible`) preservado em todos os inputs e botões.
- Manutenção de 100% de aprovação na suíte de testes automatizados existente (`pytest`).
