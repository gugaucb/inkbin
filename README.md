<div align="center">
  🌐 <b>Languages / Idiomas / 语言</b>:
  <a href="README.md">English</a> •
  <a href="README.pt-BR.md">Português (Brasil)</a> •
  <a href="README.zh-CN.md">简体中文</a>
</div>

<br>

<div align="center">

# `>_` INKBIN
### Editorial Pastebin & Anonymous Ephemeral Text Sharing

High-performance, secure, open-source editorial platform for anonymous publishing and sharing of code snippets and texts with short, obfuscated URLs, crafted under the typography and aesthetic guidelines of **INK Design System v2** and built-in internationalization (i18n).

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-000000?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-000000?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL_16_%7C_SQLite-000000?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Cache](https://img.shields.io/badge/Cache-Redis_7_%7C_In--Memory-000000?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Linter](https://img.shields.io/badge/Code_Style-Ruff-000000?style=for-the-badge&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Docker Hub](https://img.shields.io/badge/Docker_Hub-gugaucb%2Finkbin-000000?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/gugaucb/inkbin)
[![Release](https://img.shields.io/badge/Release-v0.1.0-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/gugaucb/inkbin/releases)
[![Tests](https://img.shields.io/badge/Tests-Passed-000000?style=for-the-badge&logo=pytest&logoColor=white)](tests)
[![License](https://img.shields.io/badge/License-MIT-000000?style=for-the-badge)](LICENSE)

<br>

[Visual Gallery](#-visual-gallery-and-demo) •
[Core Features](#-core-features) •
[Quickstart](#-quickstart) •
[Environment Variables](#-environment-variables) •
[Terminal Usage (cURL)](#-terminal-usage-guide-curl) •
[REST API Reference](#-rest-api-reference) •
[Architecture](#-architecture-and-structure) •
[Release Guide](#-release-and-versioning-guide) •
[Development & Contributing](#-development-and-contributing) •
[License](#-license)

</div>

---

## 📸 Visual Gallery and Demo

The Inkbin user interface is built strictly adhering to **INK Design System v2** principles, uniting high-contrast monochrome editorial typography, ergonomic touch targets, real-time counters, native multilingual support, and vector Tabler Icons.

| Editor View & Options Bar | Viewer View |
| :---: | :---: |
| <img src="docs/assets/screenshots/editor-view.png" alt="Editor View" width="550"> | <img src="docs/assets/screenshots/viewer-view.png" alt="Viewer View" width="550"> |
| *Editorial creation form featuring syntax detection, dynamic expiration, client-side encryption options (AES-256-GCM / Base64), burn-after-read switch, cyan indicators, and live counters.* | *Code reader view with metadata header, view count, quick actions (Copy Code, View Raw, Delete, Report), and syntax highlighting.* |

| Confirmation Modal with QR Code & Token | Password Challenge (Security Gate) |
| :---: | :---: |
| <img src="docs/assets/screenshots/admin-delete-modal.png" alt="Admin Delete Modal" width="550"> | <img src="docs/assets/screenshots/password-challenge.png" alt="Password Challenge" width="550"> |
| *Post-creation modal displaying the public short link with hash key, secret admin deletion key, and rendered QR Code for instant mobile scanning.* | *Challenge screen for Protected Pastes requiring cryptographic validation (Argon2id) before decrypting and rendering content.* |

<div align="center">

| Burn After Read Interstitial |
| :---: |
| <img src="docs/assets/screenshots/burn-after-read-interstitial.png" alt="Burn After Read Interstitial" width="600"> |
| *Confirmation gateway displaying publication metadata before irreversible permanent purging upon first read.* |

</div>

---

## ⚡ Core Features

- **Anonymous Creation**: Instant and streamlined sharing without registration, user accounts, email verification, or tracking telemetry.
- **Client-Side Encryption & Formats**: End-to-end zero-knowledge encryption in the browser with AES-256-GCM (keys never touch server memory) and Base64 obfuscation.
- **Burn After Read (One-Time Reading)**: Self-destructing pastes irreversibly purged immediately upon viewing.
- **Native Internationalization (i18n)**: Out-of-the-box support for English (`en` canonical default), Brazilian Portuguese (`pt-br`), and Simplified Chinese (`cn`), selectable from the sidebar footer and persisted via secure cookies.
- **Obfuscated Base62 Slugs**: Short (6–8 characters) non-sequential alphanumeric IDs preventing ID enumeration and automated scraping attacks.
- **Dynamic Expiration Policies (`EXPIRATION_OPTIONS`)**: Configurable retention periods via Docker environment variables (e.g., `1h,1d,1w,1m,never` or minutes `10m,30m`) with automated physical database and cache purging.
- **Local Browser History**: Client-side recent pastes saved in `localStorage`, featuring individual removal (`ti-x`) and complete history clearance without page reloads.
- **Protected Pastes with Argon2id**: Password protection utilizing state-of-the-art key derivation (Argon2id) with smart rate limiting after 5 consecutive incorrect attempts.
- **Admin Delete Token & QR Code**: Cryptographically random 64-character token issued at creation for permanent deletion, accompanied by a dynamic QR Code for instant mobile access.
- **Anti-Spam & Rate Limiting**: Sliding window rate limiting backed by Redis with duplicate submission suppression (SHA-256 fingerprinting).
- **Dual Data Engine with Zero-Config**: Native support for **PostgreSQL 16** (with high-performance `asyncpg` driver in production) and seamless fallback to **SQLite** (`aiosqlite` for local development without external services).
- **INK Design System v2 & Accessibility**: High-contrast monochrome editorial layout conforming to WCAG 2.1 AA, modern sans-serif typography, and Tabler Icons.

---

## 🚀 Quickstart

### Option 1: Official Docker Image (Recommended for Production & Instant Run)

Execute the pre-built multi-architecture image directly from Docker Hub:

```bash
# Standalone run with persistent volume and built-in SQLite
docker run -d \
  --name inkbin_app \
  -p 8000:8000 \
  -e APP_ENV=production \
  -e SECRET_KEY="change-this-to-a-secure-random-key-with-at-least-32-chars" \
  -v inkbin_data:/app/data \
  gugaucb/inkbin:latest
```

Or deploy the complete production cluster (Inkbin App + PostgreSQL 16 + Redis 7) using Docker Compose without needing to clone the source code:

```bash
# 1. Download official docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/gugaucb/inkbin/main/docker-compose.yml -o docker-compose.yml

# 2. Launch cluster (automatically downloads official image gugaucb/inkbin:latest)
docker compose up -d
```

Check cluster status and health:

```bash
curl -fsS http://localhost:8000/health
# Expected output: {"status":"ok","app":"inkbin"}
```

---

### Option 2: Docker Compose from Source (Development / Build Local)

When working on the source code, build and launch containers locally:

```bash
# 1. Copy environment configuration
cp .env.example .env

# 2. Build local Dockerfile and launch
docker compose up --build -d
```

View application logs in real-time:

```bash
docker compose logs -f app
```

---

### Option 3: Production Deployment with Caddy & Let's Encrypt (Automatic HTTPS)

To deploy on production servers with free SSL/TLS certificates issued and renewed automatically via Let's Encrypt / ZeroSSL, Inkbin includes **Caddy** as an integrated reverse proxy via Docker profiles (`caddy`, `proxy`, or `production`):

```bash
# 1. Configure production environment variables in your .env
cat <<EOF >> .env
COMPOSE_PROFILES=caddy
DOMAIN=paste.yourdomain.com
ACME_EMAIL=admin@yourdomain.com
BASE_URL=https://paste.yourdomain.com
EOF

# 2. Launch the stack with Caddy listening on ports 80 and 443
docker compose --profile caddy up -d
```

> [!TIP]
> **Deploy in Portainer**:
> When creating or editing your Stack in Portainer, add `COMPOSE_PROFILES=caddy` (or `production`), `DOMAIN=paste.yourdomain.com`, and `ACME_EMAIL=admin@yourdomain.com` in the **Environment variables** section. Portainer will automatically spin up the Caddy container alongside the application on ports 80 and 443.

> [!NOTE]
> **HTTPS on Local Area Network (LAN / Mobile)**:
> If you are testing via a local network IP (e.g. `192.168.15.8`) and want to enable HTTPS so browsers and mobile devices unlock the Web Crypto API, Caddy generates internal self-signed certificates by default.
> In your `.env`:
> ```env
> DOMAIN=192.168.15.8
> TLS_MODE=internal
> BASE_URL=https://192.168.15.8
> ```
> When opening `https://192.168.15.8` in Safari or Chrome, the browser will display a security warning because the certificate is self-signed:
> - **Safari**: Click **"Show Details"** ("Mostrar Detalhes") → click **"visit this website"** ("visitar este site") → confirm with password/Touch ID.
> - **Chrome**: Click **"Advanced"** → click **"Proceed to 192.168.15.8 (unsafe)"**.
> Once accepted, the browser treats the connection as a Secure Context (`window.isSecureContext = true`), fully unlocking client-side encryption.

---

### Option 4: Deployment Without Caddy (Standalone & External Reverse Proxies)

If you are already running an external reverse proxy (such as **Traefik**, **Nginx Proxy Manager**, **Cloudflare Tunnel**, or **AWS ALB**), or if you do not want Caddy managing ports 80 and 443 on your host, choose one of the two methods below:

#### Method A: Dedicated Standalone Compose File (`docker-compose.standalone.yml`)
Contains strictly the core services `app`, `db` (PostgreSQL 16), and `redis` (Redis 7), completely free of Caddy configurations, ports 80/443, and Caddy persistent volumes:

```bash
# 1. Download official standalone compose file without Caddy
curl -fsSL https://raw.githubusercontent.com/gugaucb/inkbin/main/docker-compose.standalone.yml -o docker-compose.standalone.yml

# 2. Launch stack (Inkbin exposes HTTP directly on port 8000)
docker compose -f docker-compose.standalone.yml up -d
```

> [!NOTE]
> In this configuration, point your external reverse proxy (Traefik/Nginx) to `http://<server-ip>:8000` (or `http://inkbin_app:8000` if sharing an external Docker network). Make sure your external reverse proxy passes `X-Forwarded-Proto: https` and `Host: <your-domain>` headers.

#### Method B: Standard `docker-compose.yml` (Omitting Profiles)
Because the `caddy` service in the standard `docker-compose.yml` is guarded by Docker profiles (`profiles: ["caddy", "proxy", "production"]`), running `docker compose up -d` without a profile flag will automatically start only `app`, `db`, and `redis`:

```bash
# Runs app, db, and redis without starting Caddy
docker compose up -d
```

---

### Option 5: Local Development (Zero-Config with SQLite)

Run locally without installing Docker, PostgreSQL, or Redis. Inkbin automatically falls back to in-memory caching and local SQLite database (`inkbin.db`):

```bash
# 1. Create and activate a Python 3.11+ virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install package in editable mode with development dependencies
pip install -e ".[dev]"

# 3. Start development server with hot-reload
uvicorn inkbin.main:app --reload --port 8000
```

Open your browser at [http://localhost:8000](http://localhost:8000).

---

## ⚙️ Environment Variables

Inkbin configuration is managed via Pydantic `BaseSettings` in `.env`:

| Variable | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `APP_ENV` | `string` | `development` | Runtime environment (`development`, `production`, `test`). |
| `DEBUG` | `boolean` | `true` | Enables debug mode and detailed tracebacks. |
| `SECRET_KEY` | `string` | `insecure-dev-...` | High-entropy secret key (32+ chars) used for HMAC signature of unlock tokens. |
| `HOST` | `string` | `0.0.0.0` | Network interface IP to bind. |
| `PORT` | `integer` | `8000` | HTTP service port. |
| `BASE_URL` | `string` | `http://localhost:8000` | Canonical base URL used for public share links. |
| `DATABASE_URL` | `string` | `sqlite+aiosqlite:///./inkbin.db` | SQLAlchemy Async connection string (`postgresql+asyncpg://...` or `sqlite+aiosqlite:///...`). |
| `REDIS_URL` | `string \| null` | `null` | Redis connection URL (`redis://redis:6379/0`). If omitted, uses in-memory cache and rate limiter. |
| `RATE_LIMIT_PER_MINUTE` | `integer` | `100` | Maximum requests per minute per IP address. |
| `MAX_PASTE_BYTES` | `integer` | `1048576` *(1 MB)* | Maximum permitted payload size in bytes per paste. |
| `EXPIRATION_OPTIONS` | `string` | `1h,1d,1w,1m,never` | Comma-separated list of enabled expiration options. Supports minutes (`10m`), hours (`1h`), days (`1d`), weeks (`1w`), months (`1m`), and permanent (`never`). |

---

## 💻 Terminal Usage Guide (cURL)

Inkbin is designed for command-line efficiency and automation:

### 1. Create a Simple Anonymous Paste

```bash
curl -X POST http://localhost:8000/api/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "deploy.sh",
    "content": "docker compose up -d",
    "language": "bash",
    "expiration": "1w"
  }'
```

**Response:**
```json
{
  "slug": "a8K9x2",
  "url": "http://localhost:8000/p/a8K9x2",
  "admin_delete_token": "del_9f81a7b3c2e104d88e40f5a77b2",
  "title": "deploy.sh",
  "language": "bash",
  "expires_at": "2026-10-30T17:30:00Z",
  "created_at": "2026-10-23T17:30:00Z",
  "is_protected": false
}
```

### 2. Pipe and Publish a Local File Directly

```bash
python3 -c "import json, sys; print(json.dumps({'title': 'main.py', 'language': 'python', 'content': sys.stdin.read()}))" < main.py | \
  curl -s -X POST http://localhost:8000/api/pastes \
    -H "Content-Type: application/json" \
    -d @-
```

### 3. Create a Password-Protected Paste

```bash
curl -X POST http://localhost:8000/api/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Confidential Credentials",
    "content": "API_KEY=ink_sec_9941a87b\nDB_PASS=vault_secret_99",
    "language": "yaml",
    "expiration": "1d",
    "password": "MyStrongPassword123"
  }'
```

### 4. Fetch Raw Text Content

Ideal for automation scripts, `curl | bash`, or direct downloading:

```bash
curl -s http://localhost:8000/raw/a8K9x2
# or via REST endpoint:
curl -s http://localhost:8000/api/pastes/a8K9x2/raw
```

### 5. Permanently Delete a Paste with Admin Token

Send the token generated at creation in the `X-Admin-Delete-Token` header:

```bash
curl -X DELETE http://localhost:8000/api/pastes/a8K9x2 \
  -H "X-Admin-Delete-Token: del_9f81a7b3c2e104d88e40f5a77b2"
```

---

## 🔌 REST API Reference

All responses return UTF-8 encoded JSON.

| Method | Endpoint | Headers / Parameters | Description | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/pastes` | `Content-Type: application/json` | Creates a new paste (anonymous or password-protected). | `201 Created`, `400 Bad Request`, `413 Payload Too Large`, `422 Unprocessable Entity`, `429 Too Many Requests` |
| `GET` | `/api/pastes/{slug}` | — | Retrieves paste metadata and content in JSON format. | `200 OK`, `401 Unauthorized` *(protected)*, `404 Not Found`, `451 Unavailable For Legal Reasons` |
| `GET` | `/api/pastes/{slug}/raw` | — | Retrieves raw content in plain text (`text/plain`). | `200 OK`, `401 Unauthorized`, `404 Not Found`, `451 Unavailable For Legal Reasons` |
| `GET` | `/raw/{slug}` | — | Canonical short route for raw text download. | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `POST` | `/api/pastes/{slug}/unlock` | `Content-Type: application/json` | Validates password and sets unlock cookie. | `200 OK`, `401 Unauthorized`, `404 Not Found`, `429 Too Many Requests` *(after 5 attempts)* |
| `DELETE`| `/api/pastes/{slug}` | `X-Admin-Delete-Token: <token>` | Permanently purges paste and invalidates cache. | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `POST` | `/api/pastes/{slug}/report` | `Content-Type: application/json` | Submits a moderation report (`spam`, `malware`, `leak`, `abuse`, `other`). | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `PATCH`| `/api/pastes/{slug}/deactivate`| — | Moderation deactivation of infringing content. | `200 OK`, `404 Not Found` |
| `GET` | `/set-locale/{locale}` | — | Switches interface language (`en`, `pt-br`, `cn`) and persists cookie. | `303 See Other` |
| `GET` | `/health` | — | Service healthcheck. | `200 OK` |

---

## 🏗️ Architecture and Structure

Inkbin is designed with modern asynchronous architecture and clean separation of concerns:

```
TextEditor/
├── src/
│   └── inkbin/
│       ├── config.py           # Centralized Pydantic BaseSettings configuration
│       ├── db.py               # SQLAlchemy 2 Asyncio and incremental schema migration
│       ├── expiration.py       # Dynamic duration parser and EXPIRATION_OPTIONS management
│       ├── i18n.py             # Locale resolution cascade and t() translation helper
│       ├── locales/            # Structured translation catalogs (en.json, pt-br.json, cn.json)
│       ├── models.py           # Relational ORM models (Paste, PasteReport)
│       ├── schemas.py          # Pydantic schemas for API validation and serialization
│       ├── services.py         # Domain services and database transactions
│       ├── slug.py             # Base62 unique slug generator (6-8 chars)
│       ├── security.py         # Argon2id hashing, token signing and validation
│       ├── rate_limit.py       # Async rate-limiting and anti-spam middleware
│       ├── cache.py            # Two-tier cache (L1 In-Memory / L2 Redis)
│       ├── lifecycle.py        # Expiration workers and physical purging routines
│       ├── main.py             # FastAPI entrypoint, lifespan and route mounts
│       ├── routes/
│       │   ├── api.py          # RESTful API route handlers
│       │   └── web.py          # Jinja2 template rendering and web UI routes
│       ├── static/             # INK Design System tokens (CSS), JS and fonts
│       └── templates/          # Semantic Jinja2 templates with Tabler Icons and i18n
├── tests/                      # Automated test suite with pytest
├── docs/                       # Architecture decision records, specifications and visual assets
│   ├── adr/                    # Architecture Decision Records
│   ├── agents/                 # Agent specifications and governance guidelines
│   └── assets/screenshots/     # High-resolution screenshots of the interface
├── docker-compose.yml          # Multi-container orchestration (App, PostgreSQL 16, Redis 7)
├── Dockerfile                  # Lightweight multi-stage Docker build
├── pyproject.toml              # Project dependencies and tool configurations (Ruff / pytest)
└── GLOSSARY.md                 # Domain glossary and standard terminology
```

---

## 🤝 Development and Contributing

Contributions from the open-source community are warmly welcomed! Follow these steps:

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/gugaucb/inkbin.git
cd inkbin

# Create feature branch
git checkout -b feat/my-feature

# Setup virtual environment and dependencies
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Running Automated Tests

```bash
pytest
```

### 3. Code Quality and Linting

We enforce clean formatting and typing with [Ruff](https://github.com/astral-sh/ruff):

```bash
# Lint checks
ruff check .

# Formatting checks
ruff format --check .

# Auto-formatting
ruff format .
```

---

## 🏷️ Release and Versioning Guide

Inkbin utilizes automated semantic versioning, multi-architecture image publication, and GitHub Releases:

- **Semantic Versioning (SemVer)**: Tags follow `vX.Y.Z` (e.g., `v0.1.0`).
- **Automated Docker Hub Pipeline**: Every tag push compiles multi-architecture images (`linux/amd64`, `linux/arm64`) and publishes to `gugaucb/inkbin` with tags `latest`, `X.Y.Z`, `vX.Y.Z`, and `X.Y`.
- **Automated GitHub Releases**: Creates official GitHub releases with automatically categorized commit changelogs.

To publish a new version:

```bash
# 1. Ensure tests and linters pass
pytest && ruff check .

# 2. Create annotated tag and push
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

For complete workflow details, secrets configuration, and release automation guidelines, see [Release Guide](docs/release-guide.md).

---

## 📄 License

This project is open-source software licensed under the [MIT](LICENSE) license.

<div align="center">
  <sub>Engineered for privacy, simplicity, and editorial aesthetic excellence.</sub>
</div>
