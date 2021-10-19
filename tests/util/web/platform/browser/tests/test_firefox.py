import allure

from tests.util.web.platform.browser.firefox import FireFoxManagedBrowser


@allure.feature("Test Framework Self-Check")
def test_firefox_browser():
    with FireFoxManagedBrowser("https://www.python.org") as browser:
        assert browser.session.title == "Welcome to Python.org"
