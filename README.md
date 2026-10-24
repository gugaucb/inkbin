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
[![Docker](https://img.shields.io/badge/Docker-Compose_Ready-000000?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
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
[Development & Contributing](#-development-and-contributing) •
[License](#-license)

</div>

---

## 📸 Visual Gallery and Demo

The Inkbin user interface is built strictly adhering to **INK Design System v2** principles, uniting high-contrast monochrome editorial typography, ergonomic touch targets, real-time counters, native multilingual support, and vector Tabler Icons.

| Editor View | Viewer View |
| :---: | :---: |
| <img src="docs/assets/screenshots/editor-view.png" alt="Editor View" width="550"> | <img src="docs/assets/screenshots/viewer-view.png" alt="Viewer View" width="550"> |
| *Creation form featuring Tab key indentation, syntax detection, dynamic expiration policy, optional password protection, and live character/byte counters.* | *Code reader view with metadata header, view count, quick actions (Copy Code, View Raw, Delete, Report), and syntax highlighting.* |

| Confirmation Modal & Admin Delete Token | Password Challenge (Security Gate) |
| :---: | :---: |
| <img src="docs/assets/screenshots/admin-delete-modal.png" alt="Admin Delete Modal" width="550"> | <img src="docs/assets/screenshots/password-challenge.png" alt="Password Challenge" width="550"> |
| *Post-creation modal displaying the public short link (Base62 Slug) and unrecoverable secret admin key granted to the anonymous author for permanent deletion.* | *Challenge screen for Protected Pastes requiring cryptographic validation (Argon2id) before decrypting and rendering content.* |

---

## ⚡ Core Features

- **Anonymous Creation**: Instant and streamlined sharing without registration, user accounts, email verification, or tracking telemetry.
- **Native Internationalization (i18n)**: Out-of-the-box support for English (`en` canonical default), Brazilian Portuguese (`pt-br`), and Simplified Chinese (`cn`), selectable from the sidebar footer and persisted via secure cookies.
- **Obfuscated Base62 Slugs**: Short (6–8 characters) non-sequential alphanumeric IDs preventing ID enumeration and automated scraping attacks.
- **Dynamic Expiration Policies (`EXPIRATION_OPTIONS`)**: Configurable retention periods via Docker environment variables (e.g., `1h,1d,1w,1m,never` or minutes `10m,30m`) with automated physical database and cache purging.
- **Local Browser History**: Client-side recent pastes saved in `localStorage`, featuring individual removal (`ti-x`) and complete history clearance without page reloads.
- **Protected Pastes with Argon2id**: Password protection utilizing state-of-the-art key derivation (Argon2id) with smart rate limiting after 5 consecutive incorrect attempts.
- **Admin Delete Token**: Cryptographically random 64-character token issued at creation, granting the anonymous author irrevocable permission to permanently delete their paste at any time.
- **Anti-Spam & Rate Limiting**: Sliding window rate limiting backed by Redis with duplicate submission suppression (SHA-256 fingerprinting).
- **Dual Data Engine with Zero-Config**: Native support for **PostgreSQL 16** (with high-performance `asyncpg` driver in production) and seamless fallback to **SQLite** (`aiosqlite` for local development without external services).
- **INK Design System v2 & Accessibility**: High-contrast monochrome editorial layout conforming to WCAG 2.1 AA, modern sans-serif typography, and Tabler Icons.

---

## 🚀 Quickstart

### Option 1: Docker Compose (Recommended for Production / Self-Hosting)

Launch the complete stack (FastAPI app, PostgreSQL 16 database, Redis 7 cache) in two commands:

```bash
# 1. Copy environment configuration
cp .env.example .env

# 2. Build and launch containers in background
docker compose up --build -d
```

The application is available at `http://localhost:8000`.

Check cluster health:

```bash
curl -fsS http://localhost:8000/health
# Expected output: {"status":"ok","app":"inkbin"}
```

View application logs in real-time:

```bash
docker compose logs -f app
```

---

### Option 2: Local Development (Zero-Config with SQLite)

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

## 📄 License

This project is open-source software licensed under the [MIT](LICENSE) license.

<div align="center">
  <sub>Engineered for privacy, simplicity, and editorial aesthetic excellence.</sub>
</div>
