#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import abc
import collections
import json
import logging
import sys

import selenium.webdriver

import clare
from clare import common
from clare import scraping


class BaseSubscriber(common.event_driven.interfaces.INotifyable):

    __metaclass__ = abc.ABCMeta

    def __init__(self, logger, event_name):

        """
        Parameters
        ----------
        logger : logging.Logger
        event_name : str
        """

        self._logger = logger
        self._event_name = event_name

    def notify(self, event):
        data = json.loads(event, object_pairs_hook=collections.OrderedDict)
        data['topic_name'] = (self._event_name +
                              self.__class__.__name__.replace('Subscriber', ''))
        message = json.dumps(data)
        self._logger.debug(msg=message)

    def __repr__(self):
        repr_ = '{}(logger={}, event_name="{}")'
        return repr_.format(self.__class__.__name__,
                            self._logger,
                            self._event_name)


class AttemptStartedSubscriber(BaseSubscriber):
    pass


class AttemptCompletedSubscriber(BaseSubscriber):
    pass


def main(url):

    # Global State / Singleton
    configuration = clare.configuration

    # Construct the directory path dependency.
    directory_path = configuration['scraper']['directory_path']

    # Construct the strategy dependency.
    chrome_options = selenium.webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        name='prefs',
        value={'download.default_directory': configuration['scraper']['directory_path']})
    web_driver = selenium.webdriver.Chrome(chrome_options=chrome_options)
    strategy = scraping.download_strategies.Replay(
        web_driver=web_driver,
        timeout=configuration['scraper']['strategy']['timeout'])

    # Construct the retry policy dependency.
    stop_strategy = common.retry.stop_strategies.AfterDuration(
        maximum_duration=configuration['scraper']['retry_policy']['stop_strategy']['maximum_duration'])
    wait_strategy = common.retry.wait_strategies.Fixed(
        wait_time=configuration['scraper']['retry_policy']['wait_strategy']['wait_time'])
    attempt_started_subscriber = AttemptStartedSubscriber(
        logger=logging.getLogger(name=configuration['scraper']['logger_name']),
        event_name='Download')
    attempt_completed_subscriber = AttemptCompletedSubscriber(
        logger=logging.getLogger(name=configuration['scraper']['logger_name']),
        event_name='Download')
    messaging_broker = common.event_driven.messaging.Broker(
        observable_class=common.event_driven.Observable)
    messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_STARTED.name)
    messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_COMPLETED.name)
    messaging_broker.subscribe(
        subscriber=attempt_started_subscriber,
        topic_name=common.retry.Topic.ATTEMPT_STARTED.name)
    messaging_broker.subscribe(
        subscriber=attempt_completed_subscriber,
        topic_name=common.retry.Topic.ATTEMPT_COMPLETED.name)
    retry_policy = common.retry.PolicyBuilder() \
        .with_stop_strategy(stop_strategy) \
        .with_wait_strategy(wait_strategy) \
        .continue_on_exception(scraping.exceptions.HttpError) \
        .continue_on_exception(scraping.exceptions.BattleNotCompleted) \
        .with_messaging_broker(messaging_broker) \
        .build()

    # Construct the confirm retry policy dependency.
    stop_strategy = common.retry.stop_strategies.AfterDuration(
        maximum_duration=configuration['scraper']['confirm_retry_policy']['stop_strategy']['maximum_duration'])
    wait_strategy = common.retry.wait_strategies.Fixed(
        wait_time=configuration['scraper']['confirm_retry_policy']['wait_strategy']['wait_time'])
    attempt_started_subscriber = AttemptStartedSubscriber(
        logger=logging.getLogger(name=configuration['scraper']['logger_name']),
        event_name='DownloadConfirm')
    attempt_completed_subscriber = AttemptCompletedSubscriber(
        logger=logging.getLogger(name=configuration['scraper']['logger_name']),
        event_name='DownloadConfirm')
    messaging_broker = common.event_driven.messaging.Broker(
        observable_class=common.event_driven.Observable)
    messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_STARTED.name)
    messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_COMPLETED.name)
    messaging_broker.subscribe(
        subscriber=attempt_started_subscriber,
        topic_name=common.retry.Topic.ATTEMPT_STARTED.name)
    messaging_broker.subscribe(
        subscriber=attempt_completed_subscriber,
        topic_name=common.retry.Topic.ATTEMPT_COMPLETED.name)
    confirm_retry_policy = common.retry.PolicyBuilder() \
        .with_stop_strategy(stop_strategy) \
        .with_wait_strategy(wait_strategy) \
        .continue_if_result(predicate=lambda x: x == '') \
        .continue_if_result(predicate=lambda x: '.html' not in x) \
        .continue_if_result(predicate=lambda x: '.crdownload' in x) \
        .with_messaging_broker(messaging_broker) \
        .build()

    # Construct the logger dependency.
    logger = logging.getLogger(name=configuration['scraper']['logger_name'])

    scraper = scraping.Scraper(directory_path=directory_path,
                               strategy=strategy,
                               retry_policy=retry_policy,
                               confirm_retry_policy=confirm_retry_policy,
                               logger=logger)
    scraper.scrape(url=url)
    scraper.dispose()


if __name__ == '__main__':
    main(url=sys.argv[1])
