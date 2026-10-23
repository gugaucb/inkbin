# 02 - Infraestrutura de i18n Backend, Catálogos JSON e Resolução de Locale

Status: closed
Type: task
Blocked by: 01

## Question

Como implementar o sistema de internacionalização no backend (FastAPI/Jinja2) suportando os idiomas `en` (padrão), `pt-br` e `cn` com catálogos JSON estruturados, resolução de locale em cascata e injeção do helper `t(key)` nos templates?

## Scope

1. Criar diretório `src/inkbin/locales/` com os catálogos completos:
   - `en.json`: chaves de tradução em inglês (default canônico);
   - `pt-br.json`: chaves em português brasileiro;
   - `cn.json`: chaves em chinês simplificado (简体中文).
2. Implementar `src/inkbin/i18n.py`:
   - Carregamento e cache dos arquivos JSON;
   - Função de resolução de locale na ordem:
     1. Parâmetro de query `?lang=`;
     2. Cookie `inkbin_locale`;
     3. Cabeçalho `Accept-Language`;
     4. Default `en`.
   - Helper `t(key, locale=..., **kwargs)` com interpolação de variáveis e fallback seguro para `en` caso uma chave não exista no locale solicitado.
3. Configurar endpoint `GET /set-locale/{locale}` para gravação segura do cookie `inkbin_locale` e redirecionamento para a página anterior (ou rota `/`).
4. Integrar o helper `t` e o `current_locale` aos globais/contexto do Jinja2Templates em `src/inkbin/routes/web.py`.
