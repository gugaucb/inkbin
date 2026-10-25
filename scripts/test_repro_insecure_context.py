import asyncio
import sys

from playwright.async_api import async_playwright


async def run_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        dialogs = []
        page.on("dialog", lambda d: dialogs.append(d.message) or asyncio.create_task(d.dismiss()))

        # Test 1: Access via LAN IP (Insecure context)
        lan_url = "http://192.168.15.8:8000"
        print(f"--- 1. Testing LAN IP access: {lan_url} ---")
        await page.goto(lan_url)

        is_secure = await page.evaluate("() => window.isSecureContext")
        has_subtle = await page.evaluate("() => Boolean(window.crypto && window.crypto.subtle)")
        print(f"LAN IP security: isSecureContext={is_secure}, hasCryptoSubtle={has_subtle}")
        assert not is_secure, "LAN IP should be an insecure context"
        assert not has_subtle, "Subtle crypto should be unavailable on insecure context"

        encrypt_radio = await page.query_selector("#paste-format-encrypt")
        is_disabled = await encrypt_radio.is_disabled()
        print(f"Encrypt option disabled state on LAN IP: {is_disabled}")
        assert is_disabled, "Encrypt option should be disabled on insecure context"

        # Click label for encrypt on insecure context
        dialogs.clear()
        label = await page.query_selector("label[for=paste-format-encrypt]")
        await label.dispatch_event("click")
        await page.wait_for_timeout(500)
        print(f"Dialogs after clicking disabled encrypt: {dialogs}")
        assert len(dialogs) == 1, f"Expected 1 dialog, got {dialogs}"
        assert any("HTTPS" in d or "localhost" in d or "Web Crypto" in d for d in dialogs), (
            f"Unexpected dialog message: {dialogs}"
        )

        # Submit normal plaintext paste on LAN IP
        dialogs.clear()
        import time

        await page.fill("#paste-content", f"Plaintext paste from LAN IP test {time.time()}")
        await page.click("button[type=submit]")
        await page.wait_for_timeout(2000)
        modal_visible = await page.is_visible("#success-modal")
        print(f"Modal visible after plaintext submission: {modal_visible}")
        print(f"Dialogs if any: {dialogs}")
        assert modal_visible, "Success modal should appear after valid submission"
        assert len(dialogs) == 0, f"No error dialog should appear on plaintext submit: {dialogs}"

        # Verify share URL generated on LAN IP uses request host
        share_url_input = await page.query_selector("#modal-slug-url")
        share_url_val = await share_url_input.input_value() if share_url_input else ""
        print(f"Share URL generated on LAN IP: {share_url_val}")
        assert "192.168.15.8:8000" in share_url_val, (
            f"Share URL should contain LAN IP host, got: {share_url_val}"
        )

        # Test 2: Access via localhost (Secure context)
        local_url = "http://localhost:8000"
        print(f"\n--- 2. Testing Localhost access: {local_url} ---")
        await page.goto(local_url)

        is_secure_local = await page.evaluate("() => window.isSecureContext")
        has_subtle_local = await page.evaluate(
            "() => Boolean(window.crypto && window.crypto.subtle)"
        )
        print(
            f"Localhost security: isSecureContext={is_secure_local}, hasCryptoSubtle={has_subtle_local}"
        )
        assert is_secure_local, "Localhost should be a secure context"
        assert has_subtle_local, "Subtle crypto should be available on localhost"

        encrypt_radio_local = await page.query_selector("#paste-format-encrypt")
        is_disabled_local = await encrypt_radio_local.is_disabled()
        print(f"Encrypt option disabled state on Localhost: {is_disabled_local}")
        assert not is_disabled_local, "Encrypt option should be ENABLED on localhost"

        # Select encrypt and submit on localhost
        dialogs.clear()
        await page.fill("#paste-content", f"Encrypted paste from localhost test {time.time()}")
        await page.click("label[for=paste-format-encrypt]")
        await page.click("button[type=submit]")
        await page.wait_for_timeout(2000)
        modal_visible_local = await page.is_visible("#success-modal")
        print(f"Modal visible after encrypted submission on localhost: {modal_visible_local}")
        assert modal_visible_local, (
            "Success modal should appear after encrypted submission on localhost"
        )
        assert len(dialogs) == 0, (
            f"No error dialog should appear on localhost encrypted submit: {dialogs}"
        )

        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
        await browser.close()
        return 0


if __name__ == "__main__":
    code = asyncio.run(run_tests())
    sys.exit(code)
