# -*- coding: utf-8 -*-

import collections
import logging
import sys

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import exceptions
from . import filters
from . import flush_strategies
from . import record_factories
from . import scrapers
from . import senders
from . import sources
from clare import common
from clare.common import automation
from clare.common import messaging
from clare.common import retry


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):
        # Construct the room list scraper.
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
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        scraper = scrapers.Validating(scraper=scraper, validator=validator)

        # Include retrying.
        stop_strategy = retry.stop_strategies.AfterAttempt(
            maximum_attempt=self._properties['scraper']['policy']['stop_strategy']['maximum_attempt'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['scraper']['policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['scraper']['policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='ROOM_LIST_SCRAPE')
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.InitializationFailed) \
            .continue_on_exception(exceptions.ExtractFailed) \
            .with_messaging_broker(messaging_broker) \
            .build()
        scraper = scrapers.Retrying(scraper=scraper, policy=policy)

        # Include record marshalling.
        time_zone = common.utilities.TimeZone.from_name(
            name=self._properties['time_zone']['name'])
        record_factory = record_factories.RecordFactory(
            queue_name=self._properties['queue']['name'],
            time_zone=time_zone)
        scraper = scrapers.RecordMarshallingDecorator(scraper=scraper,
                                                      factory=record_factory)

        # Include orchestration.
        logger = logging.getLogger(
            name=self._properties['scraper']['logger']['name'])
        scraper = scrapers.Orchestrating(scraper=scraper, logger=logger)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class Producer(object):

    def __init__(self, properties, sender):

        """
        Parameters
        ----------
        properties : collections.Mapping
        sender : clare.common.messaging.producer.senders.Sender
        """

        self._factory = Factory(properties=properties)
        self._properties = properties
        self._sender = sender

    def create(self):
        # Construct the producer.
        dependencies = self.create_dependencies()

        builder = messaging.producer.builders.Builder() \
            .with_source(dependencies['source']) \
            .with_sender(dependencies['sender'])
        for filter in dependencies['filters']:
            builder = builder.with_filter(filter)
        producer = builder.build()

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
        source = scrapers.BufferingSourceAdapter(
            scraper=scraper,
            url=self._properties['scraper']['url'])
        dependencies['source'] = source

        # Construct the sender.
        # Include logging.
        logger = logging.getLogger(
            name=self._properties['sender']['logger']['name'])
        sender = senders.Logging(sender=self._sender, logger=logger)
        dependencies['sender'] = sender

        # Construct the filters.
        dependencies['filters'] = list()

        # Construct the no duplicate filter.
        after_duration = flush_strategies.AfterDuration(
            maximum_duration=self._properties['filter']['flush_strategy']['maximum_duration'])
        no_duplicate = filters.NoDuplicate(flush_strategy=after_duration)
        dependencies['filters'].append(no_duplicate)

        return dependencies

    def __repr__(self):
        repr_ = '{}(properties={}, sender={})'
        return repr_.format(self.__class__.__name__,
                            self._properties,
                            self._sender)


class CommandLineArguments(Producer):

    def create_dependencies(self):
        dependencies = super(CommandLineArguments, self).create_dependencies()

        # Construct the deque source.
        deque = collections.deque(sys.argv[1:])
        time_zone = common.utilities.TimeZone.from_name(
            name=self._properties['time_zone']['name'])
        record_factory = record_factories.RecordFactory(
            queue_name=self._properties['queue']['name'],
            time_zone=time_zone)
        source = sources.Deque(deque=deque, record_factory=record_factory)
        dependencies['source'] = source

        return dependencies
