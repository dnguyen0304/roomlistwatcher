# -*- coding: utf-8 -*-

import datetime
import logging
import sys
import threading

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import lxml.html
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from clare import common
from .messaging.client import consumer
from .messaging.client import producer
from .messaging.client import records
from . import scraping
from . import applications
from . import filters
from . import flush_strategies
from . import handlers
from . import scrapers
from . import senders
from . import sources


class Record(object):

    _record_class = records.Record

    def __init__(self, queue_name, time_zone):
        self._queue_name = queue_name
        self._time_zone = time_zone

    def create(self, value=None):
        timestamp = datetime.datetime.utcnow().replace(tzinfo=self._time_zone)
        record = records.Record(queue_name=self._queue_name,
                                timestamp=timestamp,
                                value=value)
        return record

    def create_from_html(self, html):
        element = lxml.html.fragment_fromstring(html=html)
        room_path = element.get(key='href')
        record = self.create(value=room_path)
        return record

    def __repr__(self):
        repr_ = '{}(queue_name="{}", time_zone={})'
        return repr_.format(self.__class__.__name__,
                            self._queue_name,
                            self._time_zone)


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
        # Construct the message queue.
        message_queue = queue.Queue()

        # Construct the room list scraper.
        source_message_queue = queue.Queue()

        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._configuration['room_list_watcher']['scraper']['wait_context']['timeout'])
        scraper = scraping.scrapers.RoomList(web_driver=web_driver,
                                             wait_context=wait_context)

        # Include marshalling.
        queue_name = self._configuration['room_list_watcher']['queue']['name']
        name = self._configuration['common']['time_zone']['name']
        time_zone = common.utilities.TimeZone.from_name(name)
        record_factory = Record(queue_name=queue_name, time_zone=time_zone)
        scraper = scrapers.Marshalling(scraper=scraper,
                                       record_factory=record_factory)

        # Include polling.
        scraper = scraping.scrapers.Polling(
            scraper=scraper,
            wait_time=self._configuration['room_list_watcher']['scraper']['wait_time'],
            message_queue=source_message_queue)

        # Include orchestration.
        logger = logging.getLogger(
            name=self._configuration['room_list_watcher']['scraper']['logger']['name'])
        scraper = scrapers.Orchestration(scraper=scraper, logger=logger)
        worker_thread = threading.Thread(
            name='room_list_watcher.scraper',
            target=scraper.scrape,
            kwargs={'url': self._configuration['room_list_watcher']['scraper']['url']})
        source = sources.Batched(worker_thread=worker_thread,
                                 message_queue=source_message_queue)

        # Construct the producer sender with logging.
        sender = producer.internals.senders.Sender(message_queue=message_queue)
        name = self._configuration['room_list_watcher']['scraper']['logger']['name']
        logger = logging.getLogger(name=name)
        sender = senders.Logged(sender=sender, logger=logger)

        # Construct the producer filter.
        maximum_duration = self._configuration['room_list_watcher']['filter']['maximum_duration']
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
