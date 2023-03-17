from tests.util.web.platform.browser.chrome import ChromeManagedBrowser


def test_chrome_browser():
    with ChromeManagedBrowser("https://www.python.org") as browser:
        assert browser.session.title == "Welcome to Python.org"
