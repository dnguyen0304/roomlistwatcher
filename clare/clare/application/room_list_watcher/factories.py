# -*- coding: utf-8 -*-

import logging
import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import exceptions
from . import record_factories
from . import scrapers
from clare import common


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):
        # Construct the scraper.
        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._properties['scraper']['wait_context']['timeout'])
        scraper = scrapers.RoomList(web_driver=web_driver,
                                    wait_context=wait_context)

        # Include repeating.
        # This should be composed before validation so that validation
        # occurs each time instead of only once.
        scraper = scrapers.Repeating(scraper=scraper)

        # Include validation.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['scraper']['validator']['wait_context']['timeout'])
        validator = common.automation.validators.PokemonShowdown(
            wait_context=wait_context)
        scraper = scrapers.Validating(scraper=scraper, validator=validator)

        # Include retrying.
        stop_strategy = common.retry.stop_strategies.AfterAttempt(
            maximum_attempt=self._properties['scraper']['policy']['stop_strategy']['maximum_attempt'])
        wait_strategy = common.retry.wait_strategies.Fixed(
            wait_time=self._properties['scraper']['policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(name=self._properties['scraper']['policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = common.retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='RoomListScrape')
        policy = common.retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(common.automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.InitializationFailed) \
            .continue_on_exception(exceptions.ExtractFailed) \
            .with_messaging_broker(messaging_broker) \
            .build()
        scraper = scrapers.Retrying(scraper=scraper, policy=policy)

        # Include record marshalling.
        # This should be composed before queuing so that records are
        # enqueued instead of elements.
        time_zone = common.utilities.TimeZone.from_name(
            name=self._properties['time_zone']['name'])
        record_factory = record_factories.RecordFactory(
            queue_name=self._properties['queue']['name'],
            time_zone=time_zone)
        scraper = scrapers.RecordMarshallingDecorator(scraper=scraper,
                                                      factory=record_factory)

        # Include queuing.
        message_queue = queue.Queue()
        scraper = scrapers.QueuingDecorator(scraper=scraper,
                                            message_queue=message_queue)

        # Include polling.
        scraper = scrapers.PollingDecorator(
            scraper=scraper,
            wait_time=self._properties['scraper']['wait_time'])

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
