# -*- coding: utf-8 -*-

import abc

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from . import interfaces
from . import utilities
from clare import scraping


class Base(interfaces.IDisposable, interfaces.IExtractStrategy):

    __metaclass__ = abc.ABCMeta

    def __init__(self, web_driver, wait_context):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.Chrome
        wait_context : selenium.webdriver.support.ui.WebDriverWait
        """

        self._web_driver = web_driver
        self._wait_context = wait_context

    def extract(self, url):
        self._web_driver.get(url=url)

        if self._confirm_server_error():
            message = 'The connection with the target server was lost.'
            raise scraping.exceptions.HttpError(message)

        elements = self.do_extract()
        serialized_elements = self._serialize(elements=elements)
        return serialized_elements

    def _confirm_server_error(self):
        css_selector = 'body > div.ps-overlay > div > form > p:first-child'
        locator = (By.CSS_SELECTOR, css_selector)
        text_ = 'disconnected'
        condition = expected_conditions.text_to_be_present_in_element(
            locator=locator,
            text_=text_)
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            encountered_server_error = False
        else:
            encountered_server_error = True
        return encountered_server_error

    @staticmethod
    def _serialize(elements):

        """
        Parameters
        ----------
        elements : collections.Iterable

        Returns
        -------
        collections.Sequence
        """

        serialized_elements = [element.get_attribute('outerHTML')
                               for element
                               in elements]
        return serialized_elements

    @abc.abstractmethod
    def do_extract(self):

        """
        Returns
        -------
        collections.Iterable

        Raises
        ------
        clare.watching.scraping.exceptions.ExtractFailed
        """

        pass

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = '{}(web_driver={}, wait_strategy={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._wait_context)


class RoomList(Base):

    def do_extract(self):
        locator = (By.CSS_SELECTOR, 'button[name="roomlist"]')
        button = utilities.find_button(locator=locator,
                                       wait_context=self._wait_context)
        try:
            button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.ExtractFailed(message)

        locator = (By.CSS_SELECTOR, 'div.roomlist > div > div > a')
        condition = expected_conditions.presence_of_all_elements_located(
            locator=locator)
        try:
            elements = self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            elements = list()
        return elements
