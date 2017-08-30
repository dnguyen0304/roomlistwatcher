# -*- coding: utf-8 -*-

import logging

import selenium.webdriver
from clare.common import automation
from clare.common import retry
from selenium.webdriver.support.wait import WebDriverWait

from . import exceptions
from . import scrapers


class Scraper(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        clare.application.room_list_watcher.automation.scrapers.Scraper
        """

        # Create the room list scraper.
        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._properties['wait_context']['timeout'])
        scraper = scrapers.RoomList(web_driver=web_driver,
                                    wait_context=wait_context)

        # Include repeating.
        # This should be composed before validation so that validation
        # occurs each time instead of only once.
        scraper = scrapers.Repeating(scraper=scraper)

        # Include validation.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['validator']['wait_context']['timeout'])
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        scraper = scrapers.Validating(scraper=scraper, validator=validator)

        # Create the retry policy.
        stop_strategy = retry.stop_strategies.AfterAttempt(
            maximum_attempt=self._properties['retry_policy']['stop_strategy']['maximum_attempt'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['retry_policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['retry_policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name=self._properties['event']['name'])
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.InitializationFailed) \
            .continue_on_exception(exceptions.ExtractFailed) \
            .with_messaging_broker(messaging_broker) \
            .build()

        # Create the logger.
        logger = logging.getLogger(name=self._properties['logger']['name'])

        # Include orchestration.
        scraper = scrapers.Orchestrating(scraper=scraper,
                                         logger=logger,
                                         policy=policy)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
