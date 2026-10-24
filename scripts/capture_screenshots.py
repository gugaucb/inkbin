import asyncio
import os
import signal
import subprocess
import time
from pathlib import Path
from playwright.async_api import async_playwright

PORT = 8765
BASE_URL = f"http://127.0.0.1:{PORT}"
OUT_DIR = Path("/Users/gustavoluiscosta/Downloads/projetos/TextEditor/docs/assets/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def wait_for_server(url: str, timeout: float = 15.0):
    import httpx

    start = time.time()
    while time.time() - start < timeout:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{url}/health")
                if res.status_code == 200:
                    return True
        except Exception:
            pass
        await asyncio.sleep(0.3)
    return False


async def capture_all():
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    env["DATABASE_URL"] = "sqlite+aiosqlite:///./test_screenshots.db"
    env["APP_ENV"] = "development"
    env["REDIS_URL"] = ""

    if os.path.exists("test_screenshots.db"):
        os.remove("test_screenshots.db")

    proc = subprocess.Popen(
        ["./.venv/bin/uvicorn", "inkbin.main:app", "--port", str(PORT), "--host", "127.0.0.1"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        ok = await wait_for_server(BASE_URL)
        if not ok:
            print("Failed to start server!")
            return

        import httpx

        # Create public paste
        async with httpx.AsyncClient() as client:
            resp_pub = await client.post(
                f"{BASE_URL}/api/pastes",
                json={
                    "title": "infrastructure/deploy.sh",
                    "language": "bash",
                    "expiration": "1w",
                    "content": '#!/usr/bin/env bash\nset -euo pipefail\n\n# Inkbin Zero-Downtime Deployment & Health Verification\necho "==> Pulling official image from Docker Hub (gugaucb/inkbin:latest)..."\ndocker compose pull app redis db\n\necho "==> Initializing PostgreSQL schemas and migrations..."\ndocker compose run --rm app python -m inkbin.db_init\n\necho "==> Starting high-performance web cluster..."\ndocker compose up -d\n\necho "==> Verifying system health and readiness probe..."\ncurl -fsS http://localhost:8000/health\n\necho "==> Deploy finished successfully under INK Design System v2!"\n',
                },
            )
            pub_data = resp_pub.json()
            pub_slug = pub_data["slug"]

            # Create protected paste
            resp_prot = await client.post(
                f"{BASE_URL}/api/pastes",
                json={
                    "title": "Secrets & Production Vault Configuration",
                    "language": "yaml",
                    "expiration": "1d",
                    "password": "supersecretpassword123",
                    "content": "database:\n  host: db.internal.net\n  user: ink_admin\n  port: 5432\napi_token: ink_sec_live_9a8f27c3d1\ncluster_nodes:\n  - node-01.prod.lan\n  - node-02.prod.lan",
                },
            )
            prot_data = resp_prot.json()
            prot_slug = prot_data["slug"]

            # Create burn-after-read paste
            resp_burn = await client.post(
                f"{BASE_URL}/api/pastes",
                json={
                    "title": "Ephemeral Encryption Key Exchange (One-Time Access)",
                    "language": "text",
                    "expiration": "1h",
                    "burn_after_read": True,
                    "content": "MASTER_RECOVERY_KEY=a7f29b01c3d4e5f60718293a4b5c6d7e8f901234\nTOKEN_SECRET=ink_live_ephemeral_token_burn_guard\n",
                },
            )
            burn_data = resp_burn.json()
            burn_slug = burn_data["slug"]

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={"width": 1280, "height": 840}, device_scale_factor=1.5
            )
            page = await context.new_page()

            # 1. Editor View
            print("Capturing editor-view.png...")
            await page.goto(f"{BASE_URL}/")
            await page.wait_for_selector("#paste-content")
            await page.fill("#paste-title", "main.py — Async Web Service Pipeline")
            await page.select_option("#paste-expiration", "1w")

            sample_python = '''import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI, Depends
from inkbin.security import verify_admin_token

app = FastAPI(title="Inkbin Pipeline", version="2.0.0")

@app.get("/stream")
async def stream_events() -> AsyncGenerator[str, None]:
    """Stream real-time editorial events with low latency."""
    for step in range(1, 6):
        await asyncio.sleep(0.4)
        yield f"event: step_{step} verified\\n\\n"
'''
            await page.fill("#paste-content", sample_python)

            # Activate AES-256-GCM format radio
            await page.click("label[for='paste-format-encrypt']")
            # Activate Burn after read checkbox
            await page.click("label[for='paste-burn-after-read']")

            # Dispatch input to update character and byte counters
            await page.evaluate("""() => {
                const el = document.getElementById('paste-content');
                el.dispatchEvent(new Event('input', { bubbles: true }));
            }""")
            await asyncio.sleep(0.8)
            await page.screenshot(path=str(OUT_DIR / "editor-view.png"), full_page=False)

            # 2. Admin Delete Modal View with rendered QR Code
            print("Capturing admin-delete-modal.png...")
            await page.evaluate("""() => {
                const mockData = {
                    url: 'http://localhost:8000/p/a8K9x2',
                    admin_delete_token: 'del_9f81a7b3c2e104d88e40f5a77b2'
                };
                showSuccessModal(mockData, 'k7x9L2mP4qR8vW1zY3');
            }""")
            await asyncio.sleep(0.8)
            await page.screenshot(path=str(OUT_DIR / "admin-delete-modal.png"), full_page=False)

            # Close modal
            await page.evaluate("() => closeSuccessModal()")

            # 3. Viewer View
            print("Capturing viewer-view.png...")
            await page.goto(f"{BASE_URL}/p/{pub_slug}")
            await page.wait_for_selector(".viewer-card")
            await asyncio.sleep(0.8)
            await page.screenshot(path=str(OUT_DIR / "viewer-view.png"), full_page=False)

            # 4. Password Challenge View
            print("Capturing password-challenge.png...")
            await page.goto(f"{BASE_URL}/p/{prot_slug}")
            await page.wait_for_selector("#unlock-form")
            await page.fill("#unlock-password", "supersecretpassword123")
            await asyncio.sleep(0.8)
            await page.screenshot(path=str(OUT_DIR / "password-challenge.png"), full_page=False)

            # 5. Burn-after-read Interstitial View
            print("Capturing burn-after-read-interstitial.png...")
            await page.goto(f"{BASE_URL}/p/{burn_slug}")
            await page.wait_for_selector(".viewer-card, #burn-reveal-form")
            await asyncio.sleep(0.8)
            await page.screenshot(
                path=str(OUT_DIR / "burn-after-read-interstitial.png"), full_page=False
            )

            await browser.close()
            print("All screenshots successfully captured!")

    finally:
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
        if os.path.exists("test_screenshots.db"):
            os.remove("test_screenshots.db")


if __name__ == "__main__":
    asyncio.run(capture_all())
