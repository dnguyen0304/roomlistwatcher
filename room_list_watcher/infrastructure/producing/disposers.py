# -*- coding: utf-8 -*-

import abc


class WebDriverDisposer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self, web_driver):

        """
        Garbage collect the resource.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver

        Returns
        -------
        None
        """

        raise NotImplementedError


class ChromeWebDriver(WebDriverDisposer):

    def dispose(self, web_driver):

        """
        Garbage collect the resource.

        Parameters
        ----------
        web_driver : selenium.webdriver.chrome.webdriver.WebDriver

        Returns
        -------
        None
        """

        web_driver.quit()


class Capturing(WebDriverDisposer):

    def __init__(self, disposer, file_path_generator):

        """
        Extension to include capturing screenshots.

        Parameters
        ----------
        disposer : room_list_watcher.infrastructure.producing.disposers.WebDriverDisposer
        file_path_generator : typing.Generator[str, None, None]
        """

        self._disposer = disposer
        self._file_path_generator = file_path_generator

    def dispose(self, web_driver):
        file_path = next(self._file_path_generator)
        web_driver.get_screenshot_as_file(file_path)
        self._disposer.dispose(web_driver=web_driver)
