# Spec: Vitrine de Recursos e Garantias da Plataforma (Platform Features & Guarantees Showcase)

## 1. Visão Geral
Adição de uma vitrine editorial monocromática de recursos, garantias de privacidade, expiração e facilidades para desenvolvedores diretamente na página principal do Inkbin (`editor.html`), destacando o valor da plataforma sem comprometer a clareza e usabilidade da área de criação de paste.

O design e a implementação seguem estritamente as diretrizes do **INK Design System v2** (`docs/agents/INK_Design_System_v2.md`), com foco especial na **ergonomia em dispositivos móveis e telas menores** (`<= 639px`), assegurando legibilidade, alvos táteis adequados e ausência total de transbordamento horizontal.

## 2. Pilares de Conteúdo e Garantias da Plataforma

A vitrine agrupa e apresenta os 8 compromissos fundamentais do Inkbin:

1. **Anonymous Creation (Criação Anônima)**: Sem contas, sem necessidade de cadastro, sem retenção de IPs brutos em banco ou logs.
2. **Encrypted Sharing (Compartilhamento Protegido)**: Proteção por senha opcional com derivação criptográfica Argon2id e bloqueio anti-brute-force.
3. **Auto-expiry (Expiração Automática)**: Ciclos de retenção configuráveis (de 10 minutos a 1 semana ou nunca), com expurgo físico programado.
4. **Developer Ready (Pronto para Desenvolvedores)**: API REST completa em JSON, suporte nativo a cURL no terminal e visualização raw (`/raw/{slug}`).
5. **Privacy Focused (Foco em Privacidade)**: Sem cookies de rastreamento, sem scripts de telemetria ou analytics terceiros.
6. **Syntax Highlighting (Destaque de Sintaxe)**: Suporte a mais de 100 linguagens de programação com visualização editorial e numeração de linhas.
7. **No Sign-up / You Stay in Control (Sem Cadastro)**: Acesso livre a 100% dos recursos da plataforma sem barreiras de entrada.
8. **Admin Delete Token (Token de Exclusão Único)**: Chave secreta de 64 caracteres emitida na publicação, garantindo controle irrevogável de remoção imediata.

## 3. Requisitos de Telas Menores e Responsividade

Conforme diretriz explícita ("privilegiar as funcionalidades em telas menores"):

- **Mobile (`<= 639px`)**:
  - Grid de 1 ou 2 colunas compactas com cards de baixa estatura.
  - Alvos de interação e visualização confortáveis (alvo mínimo de toque de 44px quando clicável/expansível).
  - Posicionamento abaixo das ações de publicação do editor, garantindo que o usuário consiga publicar seu texto antes de rolar até as garantias.
  - Tipografia proporcional (`12px–13px`), espaçamentos contidos (`--space-3` a `--space-4`) e sem quebras de layout.
- **Tablet (`640–1023px`)**:
  - Grid de 2 a 3 colunas auto-ajustáveis com espaçamento consistente (`--space-4`).
- **Desktop e Wide (`>= 1024px`)**:
  - Grid balanceado de 4 colunas com micro-hover sutil monocromático (`border-color: var(--border-focus)`).

## 4. Requisitos de Internacionalização (i18n)

Todas as strings, títulos, ícones e descrições devem constar nos três catálogos de tradução:
- `src/inkbin/locales/en.json` (canonical default)
- `src/inkbin/locales/pt-br.json`
- `src/inkbin/locales/cn.json`

## 5. Requisitos de Qualidade e Acessibilidade
- Marcação semântica com `<section>` e atributos ARIA (`aria-labelledby`).
- Uso de ícones vetoriais Tabler com atributos de acessibilidade (`aria-hidden="true"`).
- 100% de aprovação na suíte de testes (`pytest`).
