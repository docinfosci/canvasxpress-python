"""
Fixtures for the platform tests: a headless Chromium browser, and a page with
the known window size every capture uses.
"""

import pytest

from tests.functional.platform.visual import VIEWPORT

# Chromium switches that keep captures alike between machines: no scrollbars,
# which differ by platform, a fixed colour profile, and no font hinting.
_CHROMIUM_ARGS = [
    "--hide-scrollbars",
    "--force-color-profile=srgb",
    "--font-render-hinting=none",
    "--disable-gpu",
]


@pytest.fixture(scope="session")
def browser():
    """
    A headless Chromium browser for the session.

    Skips when Playwright is not installed, and fails with instructions when it
    is installed without its browser.
    """
    sync_api = pytest.importorskip("playwright.sync_api")

    with sync_api.sync_playwright() as playwright:
        try:
            chromium = playwright.chromium.launch(headless=True, args=_CHROMIUM_ARGS)
        except Exception as error:
            pytest.fail(
                "Headless Chromium could not start. Install it with:"
                f" python -m playwright install chromium\n{error}"
            )

        yield chromium
        chromium.close()


@pytest.fixture
def page(browser):
    """
    A page in a fresh browser context with a 1920x1080 window at a device pixel
    ratio of 1, so a capture has the same pixel size on every platform,
    including high-density displays.
    """
    context = browser.new_context(
        viewport=VIEWPORT,
        device_scale_factor=1,
        color_scheme="light",
        locale="en-US",
        timezone_id="UTC",
        reduced_motion="reduce",
    )
    page = context.new_page()
    yield page
    context.close()
