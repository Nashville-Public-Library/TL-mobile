import subprocess
import time

from playwright.sync_api import Browser, BrowserContext
import pytest
import requests

@pytest.fixture(scope="session")
def server():
    
    command = ["flask", "run"]
    start = subprocess.Popen(command)
    server_URL = "http://127.0.0.1:5000"

    timeout = 12
    start_time = time.time()
    while True:
        try:
            req = requests.get(server_URL)
            if req.status_code == 200:
                break  # server is ready
        except requests.ConnectionError:
            pass

        if time.time() - start_time > timeout:
            start.terminate()
            raise RuntimeError("Flask server did not start in time")
        time.sleep(0.2)

    yield server_URL

    start.terminate()
    start.wait()

#
# ---- DESKTOP PAGE (normal browser) ----
#
@pytest.fixture(scope="function")
def desktop(browser: Browser):
    context: BrowserContext = browser.new_context(
        viewport={"width": 1280, "height": 800},
        is_mobile=False,
        has_touch=False,
    )
    page = context.new_page()
    yield page
    context.close()

#
# ---- MOBILE NOT INSTALLED ----
#
@pytest.fixture(scope="function")
def mobile_not_installed(browser: Browser, server):
    context = browser.new_context(
    viewport={"width": 393, "height": 852},
    is_mobile=True,
    has_touch=True,
    )

    page = context.new_page()
    page.goto(server)
    yield page
    context.close()

#
# ---- MOBILE INSTALLED PWA PAGE ----
#
@pytest.fixture(scope="function")
# thank you ChatGPT
def mobile_installed(browser: Browser, server):
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        is_mobile=True,
        has_touch=True,
    )

    page = context.new_page()

    # Simulate "installed / standalone" mode
    page.add_init_script("""
        // Force display-mode: standalone
        const origMatchMedia = window.matchMedia;
        window.matchMedia = (query) => {
            if (query === '(display-mode: standalone)') {
                return {
                    matches: true,
                    media: query,
                    onchange: null,
                    addListener: () => {},
                    removeListener: () => {},
                    addEventListener: () => {},
                    removeEventListener: () => {},
                    dispatchEvent: () => false,
                };
            }
            return origMatchMedia(query);
        };

        // Fake iOS standalone flag
        Object.defineProperty(window.navigator, 'standalone', {
            value: true,
            configurable: true
        });

        // Kill orientation overlay. For some reason this interrupts click events...
        const hideOverlay = () => {
            const el = document.getElementById('orientationChange');
            if (el) {
                el.style.display = 'none';
                el.style.pointerEvents = 'none';
                el.style.opacity = 0;
            }
        };

        document.addEventListener("DOMContentLoaded", hideOverlay);
        new MutationObserver(hideOverlay).observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    """)

    page.goto(server)

    # wait until Service Worker is registered and in charge of the window.
    page.wait_for_function("""
        () =>
            'serviceWorker' in navigator &&
            navigator.serviceWorker.controller !== null
    """, timeout=15000)

    yield page
    context.close()


