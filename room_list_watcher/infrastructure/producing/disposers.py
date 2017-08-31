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
        web_driver : selenium.webdriver.Chrome

        Returns
        -------
        None
        """

        web_driver.quit()


class CapturingWebDriver(WebDriverDisposer):

    def __init__(self, disposer, generator):

        """
        Extension to include capturing screenshots.

        Parameters
        ----------
        disposer : room_list_watcher.infrastructure.producing.disposers.WebDriverDisposer
        generator : room_list_watcher.infrastructure.producing.generators.FilePathGenerator
            Generator for creating file paths.
        """

        self._disposer = disposer
        self._generator = generator

    def dispose(self, web_driver):
        file_path = self._generator.generate()
        web_driver.get_screenshot_as_file(file_path)
        self._disposer.dispose(web_driver=web_driver)
