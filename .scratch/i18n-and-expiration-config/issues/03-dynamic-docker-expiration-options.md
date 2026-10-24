# 03 - Parametrização Dinâmica de Expiração via Docker e Backend (EXPIRATION_OPTIONS)

Status: closed
Type: task
Blocked by: 02

## Question

Como flexibilizar as políticas de expiração do Inkbin através da variável de ambiente `EXPIRATION_OPTIONS` no Docker/Settings, permitindo ao operador definir prazos customizados com parser dinâmico e validação estrita na API?

## Scope

1. Adicionar `EXPIRATION_OPTIONS: str = "1h,1d,1w,1m,never"` em `src/inkbin/config.py` (classe `Settings`).
2. Atualizar `.env.example` e `docker-compose.yml` documentando a variável e expondo-a ao container `app`.
3. Implementar módulo ou utilitário `src/inkbin/expiration.py`:
   - Parser de durações flexíveis suportando:
     - Minutos: `m` (ex: `10m`, `30m`)
     - Horas: `h` (ex: `1h`, `12h`)
     - Dias: `d` (ex: `1d`, `7d`)
     - Semanas: `w` (ex: `1w`, `2w`)
     - Meses: `M` ou `mo` ou `m` (tratando `1m` como 30 dias quando referente a mês ou mapeado)
     - Permanente: `never`
   - Cálculo seguro de `expires_at: datetime | None` a partir do token de duração.
4. Atualizar o schema `PasteCreateRequest` em `src/inkbin/schemas.py`:
   - Validar dinamicamente se o campo `expiration` informado pertence à lista ativa definida em `settings.EXPIRATION_OPTIONS`.
   - Se omitido, assumir `never` (se habilitado) ou a primeira opção configurada.
   - Rejeitar com status HTTP 422 qualquer opção não listada em `EXPIRATION_OPTIONS`.
5. Expor função auxiliar para obter as opções ativas com seus respectivos tokens de tradução i18n para renderização nos formulários.
