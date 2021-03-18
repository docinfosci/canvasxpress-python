from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from tests.util.web.platform.browser.generic import ManagedBrowser


class FireFoxManagedBrowser(
    ManagedBrowser
):
    """
    FireFoxManagedBrowser provides a FireFox edition of ManagedTestBrowser
    for use in Selenium based tests.
    """

    def __init__(self, url: str):
        """
        Initializes the FireFoxManagedBrowser to anticipate sessions targeting
        the provided URL.
        :param url: The URL to target when establishing new sessions.
        """
        super().__init__(
            url
        )
        self.platform = "firefox"

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return str(
            {
                'url': self.url,
                'platform': self.platform,
                'headless': self.headless,
                'remote_browser': f"{self.remote_browser}:"
                                  f"{self.remote_browser_port}",
                'session_active': self.session_active(),
            }
        )

    def _get_firefox_profile(self) -> FirefoxProfile:
        """
        Provides a FirefoxProfile object suitable for a FireFox webdriver
        session.  Specifically:
        - The download manager is hidden
        - Download actions are accepted by default for:
            text/plain
        - The download dir is set to /tmp
        :return:
        """

        profile = webdriver.FirefoxProfile()

        profile.set_preference(
            "browser.download.folderList",
            2
        )
        profile.set_preference(
            "browser.download.manager.showWhenStarting",
            False
        )
        profile.set_preference(
            "browser.download.dir",
            '/tmp'
        )
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "text/plain"
        )

        return profile

    def _get_firefox_options(self) -> Options:
        """
        Provides an Options object suitable for initializing a FireFox
        webdriver session.  At this time defaults are used.
        :return:
        """
        opts = Options()
        opts.headless = self.headless
        return opts

    def get_new_session(self):
        """
        Overrides _get_browser_session to provide an initialized FireFox
        webdriver object ready for a new session.
        :return: A FireFox webdriver object
        """
        return Firefox(
            options=self._get_firefox_options(),
            firefox_profile=self._get_firefox_profile(),
        )

    def get_new_browser(self, url, remote=False):
        """
        Overrides get_new_browser to provide a FireFoxManagedBrowser.
        :return: A Chrome webdriver object
        """
        browser = FireFoxManagedBrowser(url)
        browser.remote_browser = remote
        return browser
