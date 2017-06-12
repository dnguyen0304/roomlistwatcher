# -*- coding: utf-8 -*-

import logging
import sys
import threading

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from .messaging.client import consumer
from .messaging.client import producer
from . import scraping
from . import applications
from . import filters
from . import flush_strategies
from . import handlers
from . import scrapers
from . import senders
from . import sources


class Application(object):

    def __init__(self, configuration):
        self._configuration = configuration

    @classmethod
    def from_configuration(cls, configuration):

        """
        Parameters
        ----------
        configuration : collections.Mapping
        """

        application_factory = cls(configuration=configuration)
        return application_factory

    def create(self):
        configuration = self._configuration['room_list_watcher']

        # Construct the message queue.
        message_queue = queue.Queue()

        # Construct the producer source.
        source_message_queue = queue.Queue()

        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._configuration['room_list_watcher']['scraper']['wait_context']['timeout'])
        scraper = scraping.scrapers.RoomList(web_driver=web_driver,
                                             wait_context=wait_context)
        scraper = scraping.scrapers.SerializedElements(scraper=scraper)
        scraper = scraping.scrapers.Polling(
            scraper=scraper,
            wait_time=self._configuration['room_list_watcher']['scraper']['wait_time'],
            message_queue=source_message_queue)
        logger = logging.getLogger(
            name=self._configuration['room_list_watcher']['scraper']['logger']['name'])
        scraper = scrapers.Orchestration(scraper=scraper, logger=logger)
        worker_thread = threading.Thread(
            name='room_list_watcher.scraper',
            target=scraper.scrape,
            kwargs={'url': self._configuration['room_list_watcher']['kwargs']['url']})
        source = sources.Batched(worker_thread=worker_thread,
                                 message_queue=source_message_queue)

        # Construct the producer sender with logging.
        sender = producer.internals.senders.Sender(message_queue=message_queue)
        logger = logging.getLogger(name=configuration['scraper']['logger']['name'])
        sender = senders.Logged(sender=sender, logger=logger)

        # Construct the producer filter.
        maximum_duration = configuration['filter']['maximum_duration']
        after_duration = flush_strategies.AfterDuration(
            maximum_duration=maximum_duration)
        no_duplicate = filters.NoDuplicate(flush_strategy=after_duration)

        # Construct the producer.
        room_list_watcher = producer.builders.Builder().with_source(source) \
                                                       .with_sender(sender) \
                                                       .with_filter(no_duplicate) \
                                                       .build()
        room_list_watcher = threading.Thread(name='room_list_watcher',
                                             target=room_list_watcher.produce)
        room_list_watcher.daemon = True

        # Construct the consumer fetcher.
        fetcher = consumer.internals.fetchers.Fetcher(message_queue=message_queue)

        # Construct the consumer handler.
        handler = handlers.Print()

        # Construct the consumer.
        simple_consumer = consumer.builders.Builder().with_fetcher(fetcher) \
                                                     .with_handler(handler) \
                                                     .build()
        simple_consumer = threading.Thread(target=simple_consumer.consume,
                                           kwargs={'interval': 0.1, 'timeout': None})
        simple_consumer.daemon = True

        # Construct the application.
        application = applications.Default(producer=room_list_watcher,
                                           consumer=simple_consumer)

        return application
