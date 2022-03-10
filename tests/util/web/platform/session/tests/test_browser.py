import allure
import pytest

from typing import List

# Workaround for PyCharm import bug related to pytest fixtures
from tests.util.web.platform.browser.generic import ManagedBrowser
from tests.util.web.platform.session.browser import browsers

_pycharm_pytest_fixture_import_workaround_browsers = browsers


@allure.feature("Test Framework Self-Check")
@pytest.mark.parametrize("browsers", ["https://www.python.org"], indirect=True)
def test_browser_sessions_for_tests(browsers: List[ManagedBrowser]):
    for browser in browsers:
        assert browser.session.title == "Welcome to Python.org"
