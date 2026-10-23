# 04 - Internacionalização Completa dos Templates Jinja2 e Seletor de Idioma na UI

Status: open
Type: task
Blocked by: 02, 03

## Question

Como substituir todos os textos literais hardcoded nos templates Jinja2 do Inkbin por chamadas internacionalizadas `t(key)` e implementar um seletor minimalista de idioma no rodapé da sidebar conforme o INK Design System v2?

## Scope

1. Atualizar `src/inkbin/templates/base.html`:
   - Traduzir skip-link, labels de navegação ("Ações", "Novo texto", "Histórico Local"), rodapé ("Sem rastreamento · Anônimo");
   - Adicionar o componente de seleção de idioma no rodapé da sidebar com opções `English`, `Português (BR)` e `简体中文 (CN)`, com ícone `ti-world` ou `ti-language`;
   - Injetar no elemento `<html>` o atributo `lang="{{ current_locale }}"`.
2. Atualizar `src/inkbin/templates/editor.html`:
   - Substituir labels de campos (Título, Linguagem, Expiração, Senha, Conteúdo do paste);
   - Renderizar o `<select id="paste-expiration">` dinamicamente com as opções oriundas de `EXPIRATION_OPTIONS`, exibindo rótulos traduzidos;
   - Traduzir textos dos botões e do modal de sucesso pós-criação.
3. Atualizar `src/inkbin/templates/viewer.html`:
   - Traduzir metadados (linhas, tamanho, expira em, visualizações);
   - Traduzir botões de ação (Copiar código, Ver raw, Novo paste, Excluir, Denunciar).
4. Atualizar telas de exceção e confirmação:
   - `delete_confirmation.html` e `password_challenge.html`;
   - Páginas de erro `404.html` e `451.html`.
