# -*- coding: utf-8 -*-

import abc

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from . import interfaces


class DownloadFailed(Exception):
    pass


class HttpError(Exception):
    pass


class title_not_equal(object):

    def __init__(self, title):
        self.title = title

    def __call__(self, web_driver):
        return self.title != web_driver.title


class Base(interfaces.IDownloadStrategy):

    __metaclass__ = abc.ABCMeta

    def __init__(self, web_driver, timeout):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.Chrome
        timeout : float
            Number of seconds to wait for the page to finish rendering.
        """

        self._web_driver = web_driver
        self._timeout = timeout

    def download(self, url):
        # (duy): Should there be logic to refresh the page?
        self._web_driver.get(url=url)

        try:
            self._confirm_rendered_page(timeout=self._timeout)
        except selenium.common.exceptions.TimeoutException:
            if self._confirm_server_error(timeout=self._timeout):
                raise HttpError
            else:
                raise DownloadFailed

        self.do_download()

    def _confirm_rendered_page(self, timeout):
        wait = WebDriverWait(self._web_driver, timeout=timeout or 0)
        condition = title_not_equal('Showdown!')
        wait.until(condition)

    def _confirm_server_error(self, timeout):
        wait = WebDriverWait(self._web_driver, timeout=timeout or 0)
        css_selector = 'body > div.ps-overlay > div > form > p:first-child'
        locator = (By.CSS_SELECTOR, css_selector)
        text_ = 'disconnected'
        condition = expected_conditions.text_to_be_present_in_element(
            locator=locator,
            text_=text_)
        try:
            wait.until(condition)
        except selenium.common.exceptions.TimeoutException:
            encountered_server_error = False
        else:
            encountered_server_error = True
        return encountered_server_error

    @abc.abstractmethod
    def do_download(self):
        pass

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = '{}(web_driver={}, timeout={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._timeout)


class Replay(Base):

    def do_download(self):
        download_button = find_download_button(web_driver=self._web_driver,
                                               timeout=self._timeout)
        download_button.click()


def find_download_button(web_driver, timeout):

    """
    Parameters
    ----------
    web_driver : selenium.webdriver.Chrome
    timeout : float
        Number of seconds to wait for the button to be clickable.

    Returns
    -------
    selenium.webdriver.remote.webelement.WebElement
        If the battle has completed.
    None
        If the battle has not yet completed.
    """

    wait = WebDriverWait(web_driver, timeout=timeout or 0)
    locator = (By.CLASS_NAME, 'replayDownloadButton')
    condition = expected_conditions.element_to_be_clickable(locator=locator)
    try:
        download_button = wait.until(condition)
    except selenium.common.exceptions.TimeoutException:
        download_button = None
    return download_button
