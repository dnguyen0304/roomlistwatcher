# -*- coding: utf-8 -*-

import collections
import logging
import sys

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import adapters
from . import exceptions
from . import filters
from . import flush_strategies
from . import marshall_strategies
from . import producers
from . import scrapers
from . import senders
from . import sources
from clare.common import automation
from clare.common import messaging
from clare.common import retry
from clare.common import utilities


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
        clare.application.room_list_watcher.scrapers.Scraper
        """

        # Construct the room list scraper.
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

        # Include orchestration.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        scraper = scrapers.Orchestrating(scraper=scraper,
                                         logger=logger,
                                         policy=policy)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class Producer(object):

    def __init__(self, infrastructure, properties):

        """
        Parameters
        ----------
        infrastructure : clare.infrastructure.infrastructures.RoomListWatcher
        properties : collections.Mapping
        """

        self._factory = _Scraper(properties=properties['scraper'])
        self._infrastructure = infrastructure
        self._properties = properties

    def create(self):
        # Construct the producer.
        dependencies = self.create_dependencies()

        producer = messaging.producer.producers.Producer(
            source=dependencies['source'],
            sender=dependencies['sender'],
            filters=dependencies['filters'])

        # Include orchestration.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        producer = producers.OrchestratingProducer(producer=producer,
                                                   logger=logger)

        return producer

    def create_dependencies(self):

        """
        Returns
        -------
        dict
        """

        dependencies = dict()

        # Construct the source.
        scraper = self._factory.create()
        message_factory = messaging.factories.Message()
        marshall_strategy = marshall_strategies.SeleniumWebElementToMessage(
            message_factory=message_factory)
        source = adapters.ScraperToBufferingSource(
            scraper=scraper,
            url=self._properties['scraper']['url'],
            marshall_strategy=marshall_strategy)
        dependencies['source'] = source

        # Construct the sender.
        sender = senders.Sender(queue=self._infrastructure.produce_to_queue)

        # Include logging.
        logger = logging.getLogger(
            name=self._properties['sender']['logger']['name'])
        sender = senders.Logging(sender=sender, logger=logger)
        dependencies['sender'] = sender

        # Construct the filters.
        dependencies['filters'] = list()

        # Construct the no duplicate filter.
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._properties['filter']['flush_strategy']['duration'])
        after_duration = flush_strategies.AfterDuration(
            countdown_timer=countdown_timer)
        no_duplicate = filters.NoDuplicateBody(flush_strategy=after_duration)
        dependencies['filters'].append(no_duplicate)

        return dependencies

    def __repr__(self):
        repr_ = '{}(infrastructure={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._properties)


class CommandLineArguments(Producer):

    def create_dependencies(self):
        dependencies = super(CommandLineArguments, self).create_dependencies()

        # Construct the deque source.
        deque = collections.deque(sys.argv[1:])
        message_factory = messaging.factories.Message()
        source = sources.Deque(deque=deque, message_factory=message_factory)
        dependencies['source'] = source

        return dependencies
