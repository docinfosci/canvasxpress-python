from typing import List

import allure
import pytest

from tests.util.web.platform.browser.chrome import ChromeManagedBrowser
from tests.util.web.platform.browser.firefox import FireFoxManagedBrowser
from tests.util.web.platform.browser.generic import ManagedBrowser

TEST_SERVER_URL = "http://localhost:8080"

def get_target_urls() -> List[str]:
    return [
        TEST_SERVER_URL,
    ]

def sessions(
        url: str = TEST_SERVER_URL,
        use_chrome=True,
        use_firefox=False
) -> ManagedBrowser:
    """
    A WebDriver generator that provides browser sessions for each of the
    automated test platform supported browsers.
    :param url: The URL with which to associate the TestBrowsers
    :return: A WebDriver for each supported browser per request
    """
    if use_chrome:
        with ChromeManagedBrowser(url) as browser:
            allure.attach(
                name=f"Info - {browser.platform} browser provided",
                body=url,
                attachment_type=allure.attachment_type.TEXT
            )
            yield browser

    if use_firefox:
        with FireFoxManagedBrowser(url) as browser:
            allure.attach(
                name=f"Info - {browser.platform} browser provided",
                body=url,
                attachment_type=allure.attachment_type.TEXT
            )
            yield browser


@pytest.fixture(
    scope='function',
    params=get_target_urls()
)
def browsers(request) -> sessions():
    """
    A test fixture that provides a set of browsres in which tests should be
    executed.  One of each type of browser is available.
    :param request: Each successive URL with which to associate the TestBrowsers
    :return:
    """
    browsers = sessions(request.param)
    yield browsers
