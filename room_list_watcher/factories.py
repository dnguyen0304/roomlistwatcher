# -*- coding: utf-8 -*-

import collections
import logging
import sys
import threading

import selenium.webdriver
from selenium.webdriver.support.wait import WebDriverWait

from . import exceptions
from . import scrapers
from .common import automation
from .common import messaging
from .common import retry
from .common import utility
from .infrastructure import producing


class _Scraper(object):

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
        room_list_watcher.scrapers.Scraper
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


class RoomListWatcher(object):

    def __init__(self, infrastructure, properties):

        """
        Parameters
        ----------
        infrastructure : room_list_watcher.infrastructure.infrastructures.RoomListWatcher
        properties : collections.Mapping
        """

        self._factory = _Scraper(properties=properties['scraper'])
        self._infrastructure = infrastructure
        self._properties = properties

    def create(self):

        """
        Create the room list watcher.

        Returns
        -------
        threading.Thread
        """

        dependencies = self.create_dependencies()

        # Create the producer.
        producer = messaging.producing.producers.Simple(
            source=dependencies['source'],
            sender=dependencies['sender'],
            filters=dependencies['filters'])

        # Include blocking.
        producer = messaging.producing.producers.Blocking(
            producer=producer,
            interval=self._properties['interval'])

        # Include orchestration.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        producer = producing.producers.Orchestrating(producer=producer,
                                                     logger=logger)

        # Create threading.
        room_list_watcher = threading.Thread(name='room_list_watcher',
                                             target=producer.produce)

        return room_list_watcher

    def create_dependencies(self):

        """
        Returns
        -------
        dict
        """

        dependencies = dict()

        # Create the source.
        scraper = self._factory.create()
        marshaller = producing.marshallers.SeleniumWebElementToString()
        source = producing.adapters.ScraperToBufferingSource(
            scraper=scraper,
            url=self._properties['scraper']['url'],
            marshaller=marshaller)
        dependencies['source'] = source

        # Create the sender.
        sender = self._infrastructure.sender

        # Include logging.
        logger = logging.getLogger(
            name=self._properties['sender']['logger']['name'])
        sender = producing.senders.Logging(sender=sender, logger=logger)
        dependencies['sender'] = sender

        # Create the filters.
        dependencies['filters'] = list()

        # Create the no duplicate filter.
        countdown_timer = utility.CountdownTimer(
            duration=self._properties['filter']['flush_strategy']['duration'])
        after_duration = producing.flush_strategies.AfterDuration(
            countdown_timer=countdown_timer)
        no_duplicate = producing.filters.NoDuplicateString(
            flush_strategy=after_duration)
        dependencies['filters'].append(no_duplicate)

        return dependencies

    def __repr__(self):
        repr_ = '{}(infrastructure={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._properties)


class CommandLineArgumentsWatcher(RoomListWatcher):

    def create_dependencies(self):
        dependencies = super(CommandLineArgumentsWatcher, self).create_dependencies()

        # Create the source.
        deque = collections.deque(sys.argv[1:])
        source = producing.sources.Deque(deque=deque)
        dependencies['source'] = source

        return dependencies
