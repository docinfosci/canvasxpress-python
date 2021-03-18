import abc
import logging
import os
import platform
from abc import abstractmethod
from os import environ
from typing import Union

import allure
import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.webkitgtk.webdriver import WebDriver

logger = logging.getLogger(__name__)
logger.setLevel(int(os.environ.get('LOG_LEVEL', 10)))


def get_show_test_browser() -> bool:
    if environ.get("SHOW_TEST_BROWSER"):
        return bool(
            int(
                environ.get("SHOW_TEST_BROWSER")
            )
        )

    else:
        return False


def get_remote_test_browser() -> bool:
    if environ.get("REMOTE_TEST_BROWSER"):
        return bool(
            int(
                environ.get("REMOTE_TEST_BROWSER")
            )
        )

    else:
        return False


def get_remote_test_browser_debug_port() -> int:
    if environ.get("REMOTE_TEST_BROWSER_PORT"):
        return int(
            environ.get("REMOTE_TEST_BROWSER_PORT")
        )

    else:
        return 9222


class GenericBrowser(
    abc.ABC
):
    """
    GenericBrowser represents a basic Webdriver instance with the ability to start
    a session using the driver's default configuration.
    """

    # _platform tracks the kind of browser, such as Chrome
    _platform: str = "Unknown"

    # _headless tracks whether new sessions will use a GUI.
    _headless: bool = not get_show_test_browser()

    # _remote_browser tracks whether an externally opened browser window
    # should be used to execute Selenium commands against
    _remote_browser: bool = get_remote_test_browser()

    # _remote_browser_port tracks the port used by the externally opened
    # browser window for Selenium interaction
    _remote_browser_port: int = get_remote_test_browser_debug_port()

    # _session_start_delay tracks how long in seconds a new session will wait
    # prior to permitting the execution of browser commands.
    _session_start_delay = 120

    # _url tracks the domain and path that the session will use.
    _url: str = ''

    @property
    def url(self) -> str:
        """
        Indicates the URL to which the browser session should be directed.
        :return: The URL
        """
        return self._url

    @property
    def platform(self) -> str:
        """
        Indicates the platform on which the browser is based, such as Chrome
        vs. FireFox.
        :return: The platform
        """
        return self._platform

    @platform.setter
    def platform(self, value: str) -> None:
        """
        Sets the platform to the specified value.
        :param value: The name of the browser platform
        :return: None
        """
        self._platform = value

    @property
    def headless(self) -> bool:
        """
        Indicates whether the driver will produce a headless (non-GUI) session.
        :return: True if the session will be headless.
        """
        return self._headless

    @property
    def remote_browser(self) -> bool:
        """
        Indicates whether the driver will use an externally controlled browser.
        :return: True if the session will interact with an external browser.
        """
        return self._remote_browser

    @remote_browser.setter
    def remote_browser(self, value: bool) -> None:
        """
        Sets remote_browser to indicate whether an attempt to connect with a
        remote session should be attempted.  Permits an override of the
        REMOTE_TEST_BROWSER environment variable.
        :param value: Indicates whether a remote session should be accessed
        :return: None
        """
        self._remote_browser = value

    @property
    def remote_browser_port(self) -> int:
        """
        Indicates the port used by the external browser.
        :return: The port number for the external browser test session
        """
        return self._remote_browser_port

    @property
    def session_start_delay(self) -> int:
        """
        Indicates the delay to be used before the session permits commands to be
        execured.  Delays are essential for slow loading content.
        :return: True if the session will delay the start of command execution.
        """
        return self._session_start_delay

    def __init__(
            self,
            url: str
    ):
        """
        Initializes the GenericBrowser to anticipate sessions targeting the
        provided URL.
        :param url: The URL to target when establishing new sessions.
        """
        self._url = url

    def __str__(self):
        return str(self.__repr__(self))

    def __repr__(self):
        return str(
            {
                'url': self.url,
                'platform': self.platform,
                'headless': self.headless,
                'remote_browser': f"{self.remote_browser}:"
                                  f"{self.remote_browser_port}",
            }
        )


class ManagedBrowser(
    GenericBrowser
):
    """
    ManagedBrowser provides a GenericBrowser that manages its resources so that
    sessions may conveniently be provided by test factories and discarded
    safely after use, such as to avoid util leaks.
    """

    # _session tracks a WebDriver instance.
    _session: Union[WebDriver, None] = None

    @property
    def session(self) -> Union[WebDriver, None]:
        return self._session

    @abstractmethod
    def get_new_session(self) -> Union[WebDriver, None]:
        """
        Provides a new session with established configurations applied.  This
        implementation is abstract and must be defined for specific drivers
        such as Chrome.
        :return: A WebDriver instance suitable for use in testing.
        """
        return None

    @abstractmethod
    def get_new_browser(self, url, remote=False) -> Union[
        'ManagedBrowser', None]:
        """
        Provides a new browser using the same type of browser (e.g., if the
        browser instance is Chrome then a new Chrome session is established)
        with the specified URL loaded.
        :param url: The URL to load in the new browser session
        :param remote: Indicates whether the browser should monitor a remote
            session if the original Object is also monitoring a remote session.
            Defaults to False.
        """
        return None

    def session_active(self) -> bool:
        """
        Indicates whether the session associated with this object is active and
        available for use in tests.
        :return: True if a session is active.
        """
        if self._session != None:
            return self._session.session_id != None
        else:
            return False

    def reset_browser_window(
            self,
            load_ready_wait_time: int = 120,
            load_ready_element_id: str = None
    ) -> None:
        """
        Closes the existing window and opens a new one.  The property url will
        be used to load an initial Web page.
        :param load_ready_wait_time: The number of seconds to wait for
            load_ready_element_id to become visible if that param is specified.
        :param load_ready_element_id: The id of an element that should be
            visible on page load.  If provided this method will attempt to wait
            for the item to become visible on the page.  If not provided then
            this method will return as soon as the general Selenium test for
            a loaded page is satisfied.
        """
        logger.info(
            f"Opening new window, and closing the old window, for {self.url}"
        )

        if self.session_active():
            self._close_session()

        self._open_session()

        self._session.get(self.url)
        if load_ready_element_id is not None:
            WebDriverWait(self._session, load_ready_wait_time).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, load_ready_element_id)
                )
            )

        allure.attach(
            name=f"New window for {self.platform} running on {os.name}",
            body=f"{self.platform} on {os.name} {platform.system()} "
                 f"{platform.release()} at {self.url}"
                 f" (remote: {self.remote_browser})"
                 f" (headless: {self.headless})",
            attachment_type=allure.attachment_type.TEXT
        )

    def __init__(self, url: str):
        """
        Initializes the ManagedBrowser to anticipate sessions targeting the
        provided URL.
        :param url: The URL to target when establishing new sessions.
        """
        super().__init__(
            url
        )

    def __str__(self):
        return str(self.__repr__(self))

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

    def _open_session(self):
        self._session: WebDriver = self.get_new_session()
        self._session.implicitly_wait(self.session_start_delay)

        # Use of a remote browser assumes that someone or something else is
        # controlling the presence of remote content.  If a non-remote browser
        # is used then this instance will fetch teh content.
        if not self.remote_browser:
            self._session.get(self.url)

            # Ensure that the process runs at a nice CPU limit when on Linux
            if "Linux" in platform.system():
                browser_pid = self._session.service.process.pid
                browser_proc = psutil.Process(browser_pid)
                logger.debug(
                    f"{self.platform}"
                    f" PID {browser_pid}"
                    f" URL {self.url}"
                    f" nice: {browser_proc.nice()}"
                )
                browser_proc.nice(15)
                logger.debug(
                    f"{self.platform}"
                    f" PID {browser_pid}"
                    f" reset nice: {browser_proc.nice()}"
                )

        allure.attach(
            name=f"New session for {self.platform} running on {os.name}",
            body=f"{self.platform} on {os.name} {platform.system()} "
                 f"{platform.release()} at {self.url}"
                 f" (remote: {self.remote_browser})"
                 f" (headless: {self.headless})",
            attachment_type=allure.attachment_type.TEXT
        )

    def _close_session(self):
        if not self.remote_browser:
            if self._session:
                self._session.close()
                self._session.quit()
                self._session = None

    def __enter__(self):
        """
        Facilitates ContextManager entry (e.g., with...) by establishing a new
        session using the pre-defined configurations for the object.
        See https://www.python.org/dev/peps/pep-0343/
        :return: A WebDriver session appropriate to the ManagedBrowser
        sub-class implementing _get_browser_session().
        """
        self._open_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Facilitates ContextManager exit (e.g., leaving with...) by closing and
        quitting the WebDriver session and resetting this object.
        See https://www.python.org/dev/peps/pep-0343/
        """
        self._close_session()
