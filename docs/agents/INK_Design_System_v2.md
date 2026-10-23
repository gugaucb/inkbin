# INK — Design System 2.0

**Status:** especificação de implementação (não significa que o software já foi construído)  
**Idioma de produto:** português brasileiro (`pt-BR`)  
**Público:** produto web de publicação de textos, Markdown e código com links compartilháveis  
**Direção:** monocromático editorial, inspirado no arranjo da imagem `referencia-visual.png`  
**Uso com Claude Code:** ler em conjunto com `../CLAUDE.md`, `COMPONENTS.md`, `PRODUCT_SPEC.md` e `IMPLEMENTATION_PLAN.md`.

> Regra decisiva: referência visual é de *layout e densidade*, não de marca ou funcionalidade. **INK** é marca de trabalho, substituível. A captura não deve ser copiada pixel a pixel nem reutilizada como imagem da UI.

## 1. Princípios e invariantes

1. **Conteúdo primeiro:** priorizar a criação, leitura, cópia e compartilhamento de textos. Navegação, cards e metadados são secundários.
2. **Ink = sem cor de destaque:** interface feita com `#0A0A0A`, `#FFFFFF` e cinzas neutros. Status distinguíveis por texto, ícone e contorno, nunca somente cor.
3. **Referência de composição:** barra lateral esquerda fina, ativa em cinza; região principal branca; blocos com bordas quase invisíveis; grandes margens laterais; listas compactas.
4. **Consistência mensurável:** usar apenas tokens documentados em `../styles/ink-tokens.css` (valores canônicos).
5. **Fluxo prioritário:** escrever → escolher opções realmente disponíveis → publicar → copiar link → ler.
6. **Acessibilidade como padrão:** navegação por teclado, foco, labels, contraste, redução de movimento, zoom e leitores de tela.
7. **Não fingir produto pronto:** não mostrar interações de servidor, autenticação, salvamento remoto, privacidade ou expiração que não estejam implementadas.

### 1.1 Mapeamento da imagem anexada

| Padrão observado | Tradução no INK | Critério de reprodução |
|---|---|---|
| Navegação fixa com ícones à esquerda | `AppSidebar` com marca, buscar, atalhos, biblioteca e conta | **248 px** desktop; borda direita neutra; seleção em cinza claro |
| Saudação grande perto do topo, em área branca | Heading de `DashboardHome`: “Seus textos, em um só lugar” para autenticados | Título 28–32 px, sem emoji; alinhamento configurável pelo layout |
| Cards horizontais de páginas recentes | `RecentPasteCard` com título, tipo e data | grade 4 colunas (adaptável), borda 1 px, raio 8 px, sem sombra |
| “My tasks” em linhas densas | `PasteListRow`: título, atualização, visibilidade, menu de ações | linhas 44–56 px, alinhamento tabular, separadores discretos |
| Dois painéis lado a lado | “Descobrir” e “Populares” | duas colunas no desktop, uma no mobile; só conteúdo público real |
| Rodapé e atalhos no menu lateral | bloco de conta + ajuda/configurações | colado à base com layout flex; não copiar o painel comercial da imagem |

**Não replicar:** nome, avatar, e-mail, textos e dados da marca mostrada na captura; informações de tarefas/sprints; uso de cor azul nas etiquetas originais; efeitos de gradiente; painéis de upsell sem relação com o produto.

## 2. Identidade e tokens

### 2.1 Paleta — valores primitivos

| Token | Valor | Uso típico |
|---|---|---|
| `--ink-0` | `#FFFFFF` | fundo da página, texto inverso |
| `--ink-25` | `#FCFCFC` | superfície quase branca |
| `--ink-50` | `#FAFAFA` | sidebar |
| `--ink-100` | `#F5F5F5` | hover leve |
| `--ink-150` | `#EEEEEE` | item ativo |
| `--ink-200` | `#E5E5E5` | bordas |
| `--ink-300` | `#D4D4D4` | bordas fortes |
| `--ink-500` | `#737373` | ícone secundário **não usar em texto pequeno sem validar contraste** |
| `--ink-600` | `#525252` | metadados / rótulos secundários |
| `--ink-700` | `#404040` | ícones fortes |
| `--ink-900` | `#171717` | texto principal |
| `--ink-950` | `#0A0A0A` | CTA principal |

**Tokens semânticos obrigatórios:** `--canvas`, `--sidebar-bg`, `--surface`, `--surface-subtle`, `--surface-hover`, `--surface-active`, `--text-primary`, `--text-secondary`, `--text-inverse`, `--border-default`, `--border-strong`, `--action-primary`, `--action-primary-hover`, `--focus-ring`, `--selection-bg`, `--overlay`.

Não escrever `color: #737373` em elementos arbitrários, não herdar o anel azul da biblioteca de componentes e não usar cor cromática em erro/sucesso. Erro = ícone de alerta + texto claro + `aria-invalid` quando aplicável; sucesso = ícone de confirmação + texto. **Contraste:** corpo ≥ 4.5:1; textos grandes ≥ 3:1; indicadores e limites de elementos críticos ≥ 3:1 onde exigível (WCAG 2.2 AA).

### 2.2 Tipografia

- UI: `Inter`, `Arial`, `Helvetica`, `sans-serif`.
- Código: `JetBrains Mono`, `SFMono-Regular`, `Consolas`, `monospace`.
- Se as fontes externas não estiverem instaladas ou licenciadas para distribuição, usar os fallbacks sem impedir a renderização.

| Estilo | Tamanho | Altura de linha | Peso | Aplicação |
|---|---:|---:|---:|---|
| `display` | 32 px | 40 px | 700 | boas-vindas/home |
| `h1` | 28 px | 36 px | 700 | título de tela |
| `h2` | 22 px | 30 px | 650 | seção |
| `h3` | 18 px | 26 px | 600 | subtítulo |
| `body` | 14 px | 22 px | 400 | navegação/controles |
| `reading` | 16 px | 27 px | 400 | conteúdo publicado |
| `small` | 13 px | 20 px | 400 | textos de apoio |
| `caption` | 12 px | 18 px | 500 | carimbos e rótulos |
| `code` | 13 px | 21 px | 400 | snippets |
| `button` | 14 px | 20 px | 600 | botões |

Aplicar `letter-spacing: -0.02em` somente em títulos grandes quando houver ganho de leitura. Nunca reduzir corpo abaixo de 12 px. Quebras em paste original devem ser preservadas; não truncar conteúdo no viewer.

### 2.3 Espaçamento, contornos e geometria

- Escala de espaçamento (px): `4, 8, 12, 16, 20, 24, 32, 40, 48, 64` (`--space-*`).
- Raio: `4px` etiqueta, `8px` controle/card, `12px` modal/painel; `9999px` pílula.
- Bordas: `1px solid var(--border-default)` na maioria dos elementos; `--border-strong` para controles de formulário.
- Sombra: proibida em cards comuns. Permitida somente em popovers/modais (`--shadow-popover`).
- Ícones: preferir Lucide, grade de 18 px (16 para badges, 20 em ações de topo), traço 1.75–2 px.
- Interações: transições discretas de 120–180 ms; zero movimento essencial; respeitar `prefers-reduced-motion`.
- Controles: altura 40 px desktop; 44 px em áreas de toque; alvos clicáveis preferencialmente ≥ 44×44 px.

### 2.4 Temas

- Tema **claro é o padrão e a base da captura**.
- Tema escuro é opcional e só deve ser exposto após implementação integral, com o seletor armazenando preferência de maneira coerente.
- Os valores do tema escuro estão em `../styles/ink-tokens.css`; não inverter imagens, screenshots ou blocos de código automaticamente.
- Se o modo escuro não fizer parte da demanda, não criar toggle sem função.

## 3. Sistema de layout

### 3.1 Breakpoints

| Faixa | Viewport | Navegação | Conteúdo | Cards recentes |
|---|---|---|---|---|
| mobile | até 639 px | drawer com backdrop | 16 px lateral | 1 coluna, ou faixa horizontal acessível quando especificada |
| tablet | 640–1023 px | drawer ou sidebar reduzida **somente se implementada** | 24 px lateral | 2 colunas |
| desktop | 1024–1439 px | sidebar de 248 px | 32 px lateral; largura máx. 1120 px | até 4 colunas |
| wide | a partir de 1440 px | sidebar de 248 px | 40 px lateral; centro 1120 px | até 4 colunas |

- Leitura do paste: coluna máxima **800 px**; editor pode ocupar até 1120 px para área de edição + configurações.
- Topbar: **64 px** desktop, **56 px** celular; deve conter título/contexto e ações, nunca propaganda invasiva.
- Não usar largura fixa em celulares; evitar overflow horizontal global. O código pode ter rolagem horizontal **dentro** do viewer.
- Sidebar com `position: sticky` ou `fixed` conforme arquitetura, mas não encobrir conteúdo nem deslocar de forma instável.
- Conteúdo deve crescer com zoom 200–400%; preferir `minmax(0,1fr)` e colunas responsivas.

### 3.2 Blueprint — Home autenticada

```text
┌──────────────────── Sidebar 248 ────────────────────┬──────────────────────────── CONTEÚDO ──────────────────────────────┐
│ INK · espaço pessoal                                │  Topbar: página / busca / conta                                     │
│ [Buscar textos]                                     │                                                                           │
│ ▣ Início (ativo)                                    │       Seus textos, em um só lugar                                   │
│ ＋ Novo texto                                       │                                                                           │
│ ◇ Explorar                                          │       Acessados recentemente                                        │
│ ─────────────────────────────────────────────────   │       [ Card ][ Card ][ Card ][ Card ]                             │
│ BIBLIOTECA                                         │                                                                           │
│ ◫ Meus textos                                       │       Meus textos                                   [Ver todos]      │
│ ◻ Rascunhos                                         │       Título                      Data     Acesso        Ações       │
│ ☆ Favoritos                                         │       ---------------------------------------------------------       │
│                                                     │       ..........................................................       │
│                                                     │                                                                           │
│ Conta / Configurações / Ajuda                       │       [Descobrir]                      [Populares]                    │
└─────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────┘
```

Quando não houver autenticação, substituir biblioteca privada por CTA honesto e atalhos de criação/exploração; não renderizar dados pessoais de exemplo. Se painel “Populares” não tiver API real, **omiti-lo**, sem inventar popularidade.

### 3.3 Blueprint — Editor

```text
[Sidebar]  Nova publicação                                      [Salvar rascunho*] [Publicar]
           Título do texto [______________________________________________________]
           [Texto simples] [Markdown] [Código]        [Linguagem, se Código]
           ┌─────────────────────────────────────────────────────────────┐ ┌─────────────┐
           │ Conteúdo com fonte apropriada, foco visível e contador     │ │ Acesso      │
           │ claro de caracteres (limite informado apenas se real).    │ │ Público     │
           │ Preview markdown opcional, nunca HTML não sanitizado.     │ │ Não listado │
           │                                                             │ │ Expiração*  │
           └─────────────────────────────────────────────────────────────┘ └─────────────┘
           *Exibir somente se implementado.
```

No mobile, painel de configurações fica **abaixo** do editor; botão publicar acessível após configurações, sem sobreposição de teclado. Um CTA fixo inferior é permitido apenas se não esconder conteúdo e se houver suporte a `safe-area-inset-bottom`.

### 3.4 Blueprint — Viewer

```text
[Marca INK]    Explorar                              [Copiar link] [Copiar texto] [Baixar*]

Título do paste
Tipo · Data real · Estado de acesso · Autor (se público/autorizado)
──────────────────────────────────────────────────────────────────────
[Conteúdo preservado, leitura 800 px / monoespaçado quando código]
──────────────────────────────────────────────────────────────────────
[Reportar*]   [Editar* somente para proprietário autenticado]
```

O viewer público pode usar layout reduzido sem sidebar, mantendo linguagem visual. Não usar analytics ou banners intercalados na leitura por padrão.

## 4. Navegação e rotas de referência

| Rota | Tela | Quem vê | Observação |
|---|---|---|---|
| `/` | Home visitante ou dashboard | todos | autenticados podem ver recentes e biblioteca |
| `/new` | Novo texto | todos | publicação por visitante depende das regras reais |
| `/explore` | Explorar | todos | apenas posts públicos vigentes |
| `/p/[slug]` | Leitor | de acordo com permissão | slug opaco; acesso validado no servidor |
| `/my-pastes` | Minha biblioteca | autenticados | não confundir com conteúdo público |
| `/drafts` | Rascunhos | autenticados | só quando há persistência real |
| `/favorites` | Favoritos | autenticados | só quando implementado |
| `/login` | Entrar | visitantes | backend de autenticação real |
| `/settings` | Configurações | autenticados | só opções implementadas |

Rotas são convenção de referência, não requerimento para modificar um projeto existente. Preferir manter rotas já adotadas, documentando equivalências.

## 5. Padrões de interação

| Elemento | Normal | Hover | Foco teclado | Disabled | Loading | Erro |
|---|---|---|---|---|---|---|
| Botão primário | fundo preto, texto branco | preto levemente mais claro | outline 2px + offset | sem clique; contraste revisado | spinner monocromático + rótulo | aviso contextual quando chamada falha |
| Botão secundário | branco, borda cinza | fundo `--surface-hover` | outline 2px | sem clique | indicador se houver ação assíncrona | aviso contextual |
| Campo de texto | borda forte | borda inalterada | foco visível | leitura opcional | não aplicável | `aria-invalid`, mensagem e orientação |
| Card navegável | borda sutil | superfície hover | foco no link semântico | não usar card falso | skeleton discreto | fallback sem exibir dados inventados |
| Menu de ações | botão com `aria-label` | hover leve | gatilho com Enter/Space | itens reais somente | quando aplicável | feedback e restauração de foco |
| Toast | texto + ícone monocromático | — | não sequestra foco | — | — | `role=alert` para falhas urgentes |

Estados combinados: `loading` prevalece sobre ação; `disabled` nunca deve ser a única explicação de um recurso bloqueado; `focus-visible` não pode depender de `hover`. Evitar animações de todo o contêiner.

## 6. Componentes e sua origem

Consultar **`COMPONENTS.md`** para propriedades tipadas e critérios de aceite. Componentes mínimos:

- Estrutura: `AppShell`, `AppSidebar`, `Topbar`, `PageContainer`, `SectionHeader`.
- Primitivas: `Button`, `IconButton`, `TextField`, `Textarea`, `SelectField`, `Tabs`, `Badge`, `Tooltip`, `Dialog`, `Toast`.
- Paste: `PasteCard`, `PasteListRow`, `PasteEditor`, `PasteSettingsPanel`, `PasteViewer`, `CopyActions`, `VisibilityBadge`, `PublishResult`.
- Estados: `EmptyState`, `ErrorState`, `LoadingSkeleton`, `ConfirmDialog`.

Ícone e rótulo de privacidade devem ser utilizados juntos; não usar badge colorido. Cada ação de excluir exige confirmação e resposta real do servidor antes de refletir sucesso definitivo.

## 7. Conteúdo, microcopy e metadados

- Títulos em estilo de frase, sem capitalização inglesa artificial: “Meus textos”, “Novo texto”, “Acessados recentemente”.
- Exemplo de convite: “Cole um texto ou escreva do zero.”
- Campos: “Título”, “Conteúdo”, “Tipo de conteúdo”, “Visibilidade”, “Expiração” (se disponível).
- CTA: “Publicar texto”, “Copiar link”, “Copiar conteúdo”, “Salvar rascunho”, “Excluir texto”.
- Toast: “Link copiado.” somente após `clipboard.writeText` resolver. Em falha, “Não foi possível copiar. Selecione o link e copie manualmente.”
- Datas: valores reais, timezone explícito no sistema; data relativa em interface é opcional, `datetime` completo acessível em tooltip/`title`.
- “Não listado” tem explicação: “Qualquer pessoa com o link pode acessar.”
- “Privado” tem explicação: “Somente pessoas autorizadas podem acessar.”, **apenas se houver controle real**.
- Informação de expiração deve informar data/hora inequívocas quando necessário, sem prometer remoção retroativa de cópias externas.
- Não exibir likes, contagens ou autores fictícios; skeleton é permitido durante carregamento real.

## 8. Acessibilidade e comportamento responsivo

- Alvo: **WCAG 2.2 AA**, com verificação automática e manual (nunca alegar conformidade sem auditoria).
- Um `h1` por página, landmarks `header`, `nav`, `main`, `aside` e labels adequadas.
- Skip link para conteúdo principal; foco visível e ordem de tabulação lógica.
- Drawer mobile: fechar com Escape, foco contido enquanto aberto, devolver foco ao gatilho, impedir navegação do fundo quando modal.
- Dialog de exclusão: texto com objeto identificável, botão de cancelar, foco inicial conservador, suporte a Escape.
- `aria-live=polite` para confirmação não urgente; `role=alert` para erros críticos.
- Não impedir copiar, selecionar, fazer zoom ou usar leitor de tela no editor/viewer.
- Teclado: Tab, Shift+Tab, Enter, Space, Escape; atalhos adicionais só com instrução visível e sem conflito com navegador/editor.
- Em 320 px e com zoom, conteúdo crítico precisa permanecer acessível; colunas colapsam; viewer de código tem scroll interno.

## 9. Regras de segurança que afetam a UI

A semântica exata de acesso, expiração, criação anônima, moderação e edição está em **`PRODUCT_SPEC.md`**. Para o designer e o frontend:

- Nunca apresentar código do usuário como HTML executável.
- A prévia Markdown exige sanitização por allowlist (além de escaping); não usar `dangerouslySetInnerHTML` com input cru.
- Acesso ao post deve ser validado na origem; esconder botão não substitui autorização.
- “Não listado” impede descoberta interna, mas o link pode circular livremente.
- Conteúdo privado não pode aparecer em busca, cache público, prerender público ou metadados abertos.
- Botões de publicar/editar/excluir ficam em estado pendente enquanto servidor confirma; reverter UI em erro.
- Se não houver backend, o trabalho de interface é **protótipo** e deve ter identificação clara; nunca gerar URL falsa de publicação.

## 10. Checklist visual com resultados observáveis

- [ ] Desktop 1440 px: sidebar de 248 px, conteúdo central máx. 1120 px, título de 28–32 px e cards em grade.
- [ ] Desktop 1280 px: sidebar estável, cards sem corte, ações alinhadas, nada de barra horizontal geral.
- [ ] Tablet 768 px: sidebar convertida em drawer/recolhida funcional; 2 colunas de cards; editor sem colisões.
- [ ] Mobile 375 e 320 px: drawer abre/fecha e gerencia foco; todos os botões essenciais utilizáveis.
- [ ] Cards normais usam borda fina, não box-shadow; ícones coerentes; nenhuma cor não neutra.
- [ ] Tab e Shift+Tab percorrem interface em sequência clara; foco sempre visível.
- [ ] Layout com fonte ampliada não perde campos, textos ou ações.
- [ ] Estados vazio, carregando, erro, sem permissão e conteúdo expirado apresentam texto específico.
- [ ] Copiar/baixar preserva exatamente o conteúdo original, sem inserir números de linha ou decoração.

## 11. Critérios de não conformidade (reprovar)

Implementação deve ser corrigida se houver: botões falsos; links de publicação simulados; dados fictícios apresentados como reais; foco azul automático; toast de sucesso antes da resposta; Markdown inseguro; acesso privado somente ocultado no cliente; quebra de linha perdida; sidebar cobrindo o editor; navegação mobile inacessível; cor cromática de biblioteca; cards sombreados; duplicações de componentes.

## 12. Notas de implementação

**Stack recomendada se iniciar do zero (decisão de projeto, não regra universal):** Next.js App Router, React, TypeScript strict, Tailwind CSS, shadcn/ui ajustado para os tokens, Lucide. **Se houver app existente, adaptar às dependências instaladas e não migrar sem demanda.**

Os documentos descrevem um sistema visual e contrato de interface. Autenticação, backend, armazenamento, regras de moderação, SEO e deploy requerem decisões de arquitetura e implementação. A definição de «V2.0» diz respeito ao **design system**, não à maturidade das funcionalidades da plataforma.

### Fontes de consulta

- Referência visual primária: `referencia-visual.png` fornecida pelo solicitante.
- Orientações do Claude Code (formato de arquivo e uso de rules): https://code.claude.com/docs/en/memory
- Fluxo de verificação e trabalho por etapas: https://code.claude.com/docs/en/best-practices
- Referências funcionais de categoria: https://justpaste.it e https://pastebin.com (não copiar marca ou interfaces).
