import platform

from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from tests.util.web.platform.browser.generic import ManagedBrowser


class ChromeManagedBrowser(ManagedBrowser):
    """
    ChromeManagedBrowser provides a Chrome edition of ManagedTestBrowser
    for use in Selenium based tests.
    """

    def __init__(self, url: str):
        """
        Initializes the ChromeManagedBrowser to anticipate sessions targeting
        the provided URL.
        :param url: The URL to target when establishing new sessions.
        """
        super().__init__(url)
        self.platform = "chrome"

    def __str__(self):
        return str(self.__repr__())

    def __repr__(self):
        return str(
            {
                "url": self.url,
                "platform": self.platform,
                "headless": self.headless,
                "remote_browser": f"{self.remote_browser}:"
                f"{self.remote_browser_port}",
                "session_active": self.session_active(),
            }
        )

    def _get_chrome_capabilities(self) -> DesiredCapabilities:
        """
        Provides a DesiredCapabilities object suitable for a Chrome webdriver
        session.  Specifically:
        - Permit insecure SSL certs, such as what might be used in dev
        :return: A DesiredCapabilities object
        """

        capabilities = DesiredCapabilities.CHROME.copy()

        capabilities["acceptSslCerts"] = True
        capabilities["acceptInsecureCerts"] = True

        return capabilities

    def _get_chrome_options(self) -> Options:
        """
        Provides an Options object suitable for initializing a Chrome
        webdriver session.  Specifically:
        - Disable notifications
        - Do not check for default browser status
        - Download permissions and preferences
        - Safe browsing OFF
        - Headless per ManagedTestBrowser setting
        :return: An Options object
        """
        opts = Options()

        # Options for user interaction and session tracing
        opts.add_argument("--enable-logging=stderr --v=1")
        opts.add_argument("--disable-notifications")
        opts.add_argument("no-default-browser-check")

        # Options affecting memory and storage
        opts.add_argument("--no-sandbox")
        opts.add_argument("--allow-no-sandbox-job")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("download.prompt_for_download=False")
        opts.add_argument('download.default_directory="/tmp/"')

        # Options permitting local files to be read
        opts.add_argument("safebrowsing.enabled=False")

        # Options to reduce system hardware requirements
        opts.add_argument("--disable-gpu")

        if self.remote_browser:
            if platform.system() in ["Windows"]:
                opts.add_experimental_option(
                    "debuggerAddress", f"localhost:{self.remote_browser_port}"
                )
            else:
                opts.add_argument(f"--remote-debugging-port={self.remote_browser_port}")

        if self.headless or self.remote_browser:
            opts.add_argument("--headless")

        if self.headless:
            opts.add_argument("--window-size=1600,1600")

        return opts

    def get_new_session(self):
        """
        Overrides _get_browser_session to provide an initialized Chrome
        webdriver object ready for a new session.
        :return: A Chrome webdriver object
        """
        return Chrome(
            options=self._get_chrome_options(),
            desired_capabilities=self._get_chrome_capabilities(),
        )

    def get_new_browser(self, url, remote=False):
        """
        Overrides get_new_session to provide a Chrome session.
        :return: A Chrome webdriver object
        """
        browser = ChromeManagedBrowser(url)
        browser.remote_browser = remote
        return browser
