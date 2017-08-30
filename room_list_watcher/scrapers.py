# -*- coding: utf-8 -*-

from __future__ import print_function

import abc
import functools
import time

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from .common import automation
from .common import io
from .common import retry
from .common import utility


class Scraper(io.Disposable):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def scrape(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        collections.Sequence

        Raises
        ------
        room_list_watcher.common.automation.exceptions.ScrapeFailed
            If the scrape failed.
        """

        pass


# There should be Initializer and Extractor classes instead of protected
# methods.
class BaseScraper(Scraper):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _initialize(self, url):

        """
        Parameters
        ----------
        url : str
        """

        pass

    @abc.abstractmethod
    def _extract(self):

        """
        Returns
        -------
        collections.Sequence
        """

        pass


class Nop(BaseScraper):

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


class RoomList(BaseScraper):

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
        room_list_watcher.common.automation.exceptions.InitializationFailed
        room_list_watcher.common.automation.exceptions.ExtractFailed
        """

        self._initialize(url=url)
        elements = self._extract()
        return elements

    def _initialize(self, url):
        self._web_driver.get(url=url)
        room_list_button = automation.utility.find_button(
            locator=(By.CSS_SELECTOR, 'button[name="roomlist"]'),
            wait_context=self._wait_context)
        try:
            room_list_button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.InitializationFailed(message)

    def _extract(self):
        # Refresh the room list.
        refresh_button = automation.utility.find_button(
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


class Orchestrating(BaseScraper):

    def __init__(self, scraper, logger, policy):

        """
        Parameters
        ----------
        scraper : room_list_watcher.scrapers.BaseScraper
        logger : logging.Logger
        policy : room_list_watcher.common.retry.policy.Policy
        """

        self._scraper = scraper
        self._logger = logger
        self._policy = policy

    def scrape(self, url):
        scrape = functools.partial(self._scraper.scrape, url=url)
        try:
            elements = self._policy.execute(scrape)
        except retry.exceptions.MaximumRetry as e:
            elements = list()
            message = utility.format_exception(e=e)
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
        repr_ = '{}(scraper={}, logger={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._logger,
                            self._policy)


class Profiling(Scraper):

    def __init__(self, scraper):

        """
        Parameters
        ----------
        scraper : room_list_watcher.scrapers.Scraper
        """

        self._scraper = scraper

    def scrape(self, url):
        started_at = time.time()
        elements = self._scraper.scrape(url=url)
        elapsed_time = time.time() - started_at
        print('Elapsed Time (in seconds):', elapsed_time)
        return elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)


class Repeating(BaseScraper):

    def __init__(self, scraper):

        """
        The web page is initialized only once.

        Parameters
        ----------
        scraper : room_list_watcher.scrapers.BaseScraper
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


class Validating(BaseScraper):

    def __init__(self, scraper, validator):

        """
        Parameters
        ----------
        scraper : room_list_watcher.scrapers.BaseScraper
        validator : room_list_watcher.common.automation.validators.PokemonShowdown
        """

        self._scraper = scraper
        self._validator = validator

    def scrape(self, url):

        """
        Raises
        ------
        room_list_watcher.common.automation.exceptions.ConnectionLost
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
