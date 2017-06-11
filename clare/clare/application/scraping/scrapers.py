# -*- coding: utf-8 -*-

import abc
import time

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from . import interfaces
from . import utilities
from clare import scraping


class Base(interfaces.IDisposable, interfaces.IScraper):

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

    def scrape(self, url):
        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        self._web_driver.get(url=url)

    @abc.abstractmethod
    def _extract(self):

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


class RepeatableBase(Base):

    __metaclass__ = abc.ABCMeta

    def __init__(self, web_driver, wait_context):

        """
        Scrape the same web page multiple times.

        The web page is initialized only once.
        """

        super(RepeatableBase, self).__init__(web_driver=web_driver,
                                             wait_context=wait_context)
        self._with_initialization = True

    def scrape(self, url):
        if self._with_initialization:
            self._initialize(url=url)
            self._with_initialization = False
        elements = self._extract()
        return elements


class PokemonShowdownBase(Base):

    __metaclass__ = abc.ABCMeta

    def _initialize(self, url):
        super(PokemonShowdownBase, self)._initialize(url=url)
        if self._confirm_server_error():
            message = 'The connection with the target server was lost.'
            raise scraping.exceptions.HttpError(message)

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


class RoomList(PokemonShowdownBase, RepeatableBase):

    def _initialize(self, url):
        super(RoomList, self)._initialize(url=url)
        locator = (By.CSS_SELECTOR, 'button[name="roomlist"]')
        button = utilities.find_button(locator=locator,
                                       wait_context=self._wait_context)
        try:
            button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.ExtractFailed(message)

    def _extract(self):
        # Refresh the room list.
        locator = (By.CSS_SELECTOR, 'button[name="refresh"]')
        button = utilities.find_button(locator=locator,
                                       wait_context=self._wait_context)
        try:
            button.click()
        except AttributeError:
            message = 'The room list refresh button could not be found.'
            raise exceptions.ExtractFailed(message)

        # Confirm the refresh operation completed.
        css_selector = 'div.roomlist > div > div:last-of-type'
        element = self._web_driver.find_element_by_css_selector(css_selector)
        condition = expected_conditions.staleness_of(element=element)
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            message = 'The room list refresh operation timed out.'
            raise exceptions.ExtractFailed(message)

        # Extract the room list.
        locator = (By.CSS_SELECTOR, 'div.roomlist > div > div > a')
        condition = expected_conditions.presence_of_all_elements_located(
            locator=locator)
        try:
            elements = self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            elements = list()

        return elements


class Polling(object):

    def __init__(self, scraper, wait_time, message_queue):

        """
        Change the scrape behavior to poll the web page instead.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        wait_time : float
            Wait time in seconds.
        message_queue : Queue.Queue
        """

        self._scraper = scraper
        self.wait_time = wait_time
        self._message_queue = message_queue

    def scrape(self, url, _sleep=time.sleep):

        """
        Parameters
        ----------
        url : str
            Web page URL.
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        while True:
            data = self._scraper.scrape(url=url)
            for item in data:
                self._message_queue.put(item=item)
            _sleep(self.wait_time)

    def __repr__(self):
        repr_ = '{}(scraper={}, wait_time={}, message_queue={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self.wait_time,
                            self._message_queue)


class SerializedElements(interfaces.IDisposable):

    def __init__(self, scraper):

        """
        Change the scrape behavior to return a sequence of serialized
        elements instead.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        """

        self._scraper = scraper

    def scrape(self, url):
        elements = self._scraper.scrape(url=url)
        serialized_elements = [element.get_attribute('outerHTML')
                               for element
                               in elements]
        return serialized_elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)
