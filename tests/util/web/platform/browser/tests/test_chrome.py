import allure

from tests.util.web.platform.browser.chrome import ChromeManagedBrowser


@allure.feature('Test Framework Self-Check')
def test_chrome_browser():
    with ChromeManagedBrowser("https://www.python.org") as browser:
        assert browser.session.title == "Welcome to Python.org"
