# -*- coding: utf-8 -*-

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from . import interfaces
from clare import common


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

    def run(self, url):

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
        room_list_button = common.automation.utilities.find_button(
            locator=(By.CSS_SELECTOR, 'button[name="roomlist"]'),
            wait_context=self._wait_context)
        try:
            room_list_button.click()
        except AttributeError:
            message = 'The room list button could not be found.'
            raise exceptions.InitializationFailed(message)

    def _extract(self):
        # Refresh the room list.
        refresh_button = common.automation.utilities.find_button(
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

    def run(self, url):

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

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._validator)


class QueuingDecorator(object):

    def __init__(self, scraper, message_queue):

        """
        Parameters
        ----------
        scraper : clare.application.room_list_watcher.interfaces.IScraper
        message_queue : Queue.Queue
        """

        self._scraper = scraper
        self._message_queue = message_queue

    def run(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        None
        """

        data = self._scraper.run(url=url)
        for item in data:
            self._message_queue.put(item=item)

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, message_queue={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._message_queue)
