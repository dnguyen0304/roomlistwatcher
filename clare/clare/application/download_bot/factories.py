# -*- coding: utf-8 -*-

import collections
import logging
import os
import uuid

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import download_bots
from . import download_validators
from . import exceptions
from . import filters
from . import handlers
from . import replay_downloaders
from . import subscribers
from clare import common
from clare.common.messaging.client import consumer


class _MessagingBrokerFactory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self, event_name):

        """
        Parameters
        ----------
        event_name : str

        Returns
        -------
        common.event_driven.messaging.Broker
        """

        # Construct the attempt started subscriber with logging.
        attempt_started_subscriber = subscribers.AttemptStarted(
            event_name=event_name)
        attempt_started_subscriber = subscribers.Logging(
            subscriber=attempt_started_subscriber,
            logger=logging.getLogger(name=self._properties['handler']['logger']['name']))

        # Construct the attempt completed subscriber with logging.
        attempt_completed_subscriber = subscribers.AttemptCompleted(
            event_name=event_name)
        attempt_completed_subscriber = subscribers.Logging(
            subscriber=attempt_completed_subscriber,
            logger=logging.getLogger(name=self._properties['handler']['logger']['name']))

        # Construct the messaging broker.
        messaging_broker = common.event_driven.messaging.Broker(
            observable_class=common.event_driven.Observable)

        # Initialize the messaging broker with topics and subscribers.
        messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_STARTED.name)
        messaging_broker.create_topic(name=common.retry.Topic.ATTEMPT_COMPLETED.name)
        messaging_broker.subscribe(
            subscriber=attempt_started_subscriber,
            topic_name=common.retry.Topic.ATTEMPT_STARTED.name)
        messaging_broker.subscribe(
            subscriber=attempt_completed_subscriber,
            topic_name=common.retry.Topic.ATTEMPT_COMPLETED.name)

        return messaging_broker

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties
        self._messaging_broker_factory = _MessagingBrokerFactory(
            properties=properties)

    def create(self):
        directory_path = os.path.join(
            self._properties['factory']['root_directory_path'],
            str(uuid.uuid4()))

        # Construct the replay downloader with validation and retrying.
        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            name='prefs',
            value={'download.default_directory': directory_path})
        web_driver = selenium.webdriver.Chrome(chrome_options=chrome_options)
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['replay_downloader']['wait_context']['timeout'])
        replay_downloader = replay_downloaders.ReplayDownloader(
            web_driver=web_driver,
            wait_context=wait_context)
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['validator']['wait_context']['timeout'])
        validator = common.automation.validators.PokemonShowdown(
            wait_context=wait_context)
        replay_downloader = replay_downloaders.Validating(
            replay_downloader=replay_downloader,
            validator=validator)
        stop_strategy = common.retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['replay_downloader']['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = common.retry.wait_strategies.Fixed(
            wait_time=self._properties['replay_downloader']['policy']['wait_strategy']['wait_time'])
        messaging_broker = self._messaging_broker_factory.create(
            event_name='ReplayDownload')
        policy = common.retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(common.automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.BattleNotCompleted) \
            .with_messaging_broker(messaging_broker) \
            .build()
        replay_downloader = replay_downloaders.Retrying(
            replay_downloader=replay_downloader,
            policy=policy)

        # Construct the download validator with retrying.
        download_validator = download_validators.DownloadValidator(
            directory_path=directory_path)
        stop_strategy = common.retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['download_validator']['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = common.retry.wait_strategies.Fixed(
            wait_time=self._properties['download_validator']['policy']['wait_strategy']['wait_time'])
        messaging_broker = self._messaging_broker_factory.create(
            event_name='DownloadValidate')
        policy_builder = common.retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .with_messaging_broker(messaging_broker)
        # Exclude intermediary and temporary files.
        policy_builder = policy_builder \
            .continue_if_result(predicate=lambda x: not x) \
            .continue_if_result(predicate=lambda x: '.html' not in x) \
            .continue_if_result(predicate=lambda x: '.crdownload' in x)
        # Wait until the replay downloader has completed.
        policy_builder = policy_builder.continue_on_exception(OSError)
        policy = policy_builder.build()
        download_validator = download_validators.Retrying(
            download_validator=download_validator,
            policy=policy)

        # Construct the download bot.
        download_bot = download_bots.DownloadBot(
            replay_downloader=replay_downloader,
            download_validator=download_validator)

        return download_bot

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class Consumer(object):

    def __init__(self, properties, fetcher):

        """
        Parameters
        ----------
        properties : collections.Mapping
        fetcher : clare.common.messaging.client.consumer.internals.fetchers.Fetcher
        """

        self._factory = Factory(properties=properties)
        self._properties = properties
        self._fetcher = fetcher

    def create(self):
        # Construct the download handler with printing.
        download_bot = self._factory.create()
        handler = handlers.Download(download_bot=download_bot)
        logger = logging.getLogger(name=self._properties['handler']['logger']['name'])
        handler = handlers.Orchestrating(handler=handler, logger=logger)

        # Construct the only generation seven metagame filter.
        only_generation_seven_metagame = filters.OnlyGenerationSevenMetagame()

        # Construct the only overused metagame filter.
        only_overused_metagame = filters.OnlyOverusedMetagame()

        # Construct the consumer.
        consumer_ = consumer.builders.Builder() \
            .with_fetcher(self._fetcher) \
            .with_handler(handler) \
            .with_filter(only_generation_seven_metagame) \
            .with_filter(only_overused_metagame) \
            .build()

        return consumer_

    def __repr__(self):
        repr_ = '{}(properties={}, fetcher={})'
        return repr_.format(self.__class__.__name__,
                            self._properties,
                            self._fetcher)
