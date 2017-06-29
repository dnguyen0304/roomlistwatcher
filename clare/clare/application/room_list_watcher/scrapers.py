# -*- coding: utf-8 -*-

from __future__ import print_function

import collections
import functools
import time

import lxml.html
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from . import interfaces
from clare import common
from clare.common import automation
from clare.common import retry
from clare.common import messaging


class Nop(interfaces.IScraper):

    def scrape(self, url):
        return list()

    def _initialize(self, url):
        pass

    def _extract(self):
        return list()

    def dispose(self):
        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class RoomList(interfaces.IScraper):

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

        """
        Raises
        ------
        clare.application.room_list_watcher.exceptions.InitializationFailed
        clare.application.room_list_watcher.exceptions.ExtractFailed
        """

        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        self._web_driver.get(url=url)
        room_list_button = automation.utilities.find_button(
            locator=(By.CSS_SELECTOR, 'button[name="roomlist"]'),
            wait_context=self._wait_context)
        try:
            room_list_button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.InitializationFailed(message)

    def _extract(self):
        # Refresh the room list.
        refresh_button = automation.utilities.find_button(
            locator=(By.CSS_SELECTOR, 'button[name="refresh"]'),
            wait_context=self._wait_context)
        try:
            refresh_button.click()
        except AttributeError:
            message = 'The refresh button could not be found.'
            raise exceptions.InitializationFailed(message)

        # Validate it has completed.
        css_selector = 'div.roomlist > div > div:last-of-type'
        element = self._web_driver.find_element_by_css_selector(css_selector)
        condition = expected_conditions.staleness_of(element=element)
        try:
            self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            message = 'The refresh operation timed out.'
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

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = '{}(web_driver={}, wait_context={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._wait_context)


class Orchestrating(interfaces.IScraper):

    def __init__(self, scraper, logger):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        logger : logging.Logger
        """

        self._scraper = scraper
        self._logger = logger

    def scrape(self, url):
        elements = list()
        try:
            elements = self._scraper.scrape(url=url)
        except retry.exceptions.MaximumRetry as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.debug(msg=message)
        return elements

    def _initialize(self, url):
        self._scraper._initialize(url=url)

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._logger)


class Repeating(interfaces.IScraper):

    def __init__(self, scraper):

        """
        The web page is initialized only once.

        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        """

        self._scraper = scraper
        self._with_initialization = True

    def scrape(self, url):
        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        if self._with_initialization:
            self._scraper._initialize(url=url)
            self._with_initialization = False

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)


class Retrying(interfaces.IScraper):

    def __init__(self, scraper, policy):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        policy : clare.common.retry.policy.Policy
        """

        self._scraper = scraper
        self._policy = policy

    def scrape(self, url):
        scrape = functools.partial(self._scraper.scrape, url=url)
        elements = self._policy.execute(scrape)
        return elements

    def _initialize(self, url):
        self._scraper._initialize(url=url)

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._policy)


class Validating(interfaces.IScraper):

    def __init__(self, scraper, validator):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        validator : clare.common.automation.validators.PokemonShowdown
        """

        self._scraper = scraper
        self._validator = validator

    def scrape(self, url):

        """
        Raises
        ------
        clare.common.automation.exceptions.ConnectionLost
            If the connection with the target server was lost.
        """

        self._initialize(url=url)
        elements = self._scraper._extract()
        return elements

    def _initialize(self, url):
        self._scraper._initialize(url=url)
        self._validator.check_connection_exists()

    def _extract(self):
        elements = self._scraper._extract()
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._validator)


class ProfilingDecorator(object):

    def __init__(self, scraper):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        """

        self._scraper = scraper

    def scrape(self, url):

        """
        Returns
        -------
        None
        """

        started_at = time.time()
        self._scraper.scrape(url=url)
        elapsed_time = time.time() - started_at
        print('Elapsed Time (in seconds):', elapsed_time)

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)


class RecordMarshallingDecorator(object):

    def __init__(self, scraper, factory):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        factory : clare.application.room_list_watcher.record_factories.RecordFactory
        """

        self._scraper = scraper
        self._factory = factory

    def scrape(self, url):

        """
        Returns
        -------
        collections.Sequence
        """

        records = list()
        elements = self._scraper.scrape(url=url)
        for element in elements:
            html = element.get_attribute('outerHTML')
            element = lxml.html.fragment_fromstring(html=html)
            room_path = element.get(key='href')
            record = self._factory.create(value=room_path)
            records.append(record)
        return records

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, factory={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._factory)


class BufferingSourceAdapter(messaging.producer.interfaces.ISource):

    def __init__(self, scraper, url):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.scrapers.RecordMarshallingDecorator
        url : str
        """

        self._scraper = scraper
        self._url = url
        self._buffer = collections.deque()

    def emit(self):
        records = self._scraper.scrape(url=self._url)
        # Use extend() followed by popleft() to have FIFO behavior as
        # with a queue. Using extendleft() followed by pop() expectedly
        # also accomplishes this goal.
        #
        # Iterating through the records in reverse is done because the
        # room list is scraped "backwards". In other words, the newest
        # rooms are at the head of the array and the oldest ones are at
        # its tail.
        self._buffer.extend(reversed(records))
        record = self._buffer.popleft()
        return record

    def __repr__(self):
        repr_ = '{}(scraper={}, url="{}")'
        return repr_.format(self.__class__.__name__, self._scraper, self._url)
