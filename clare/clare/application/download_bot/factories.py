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
from . import fetchers
from . import filters
from . import handlers
from . import replay_downloaders
from clare.common import automation
from clare.common import messaging
from clare.common import retry
from clare.common import utilities


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):
        directory_path = os.path.join(
            self._properties['factory']['root_directory_path'],
            str(uuid.uuid4()))

        # Construct the replay downloader.
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

        # Include validation.
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['replay_downloader']['validator']['wait_context']['timeout'])
        validator = automation.validators.PokemonShowdown(
            wait_context=wait_context)
        replay_downloader = replay_downloaders.Validating(
            replay_downloader=replay_downloader,
            validator=validator)

        # Include retrying.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['replay_downloader']['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['replay_downloader']['policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['replay_downloader']['policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='REPLAY_DOWNLOAD')
        policy = retry.PolicyBuilder() \
            .with_stop_strategy(stop_strategy) \
            .with_wait_strategy(wait_strategy) \
            .continue_on_exception(automation.exceptions.ConnectionLost) \
            .continue_on_exception(exceptions.BattleNotCompleted) \
            .with_messaging_broker(messaging_broker) \
            .build()
        replay_downloader = replay_downloaders.Retrying(
            replay_downloader=replay_downloader,
            policy=policy)

        # Construct the download validator.
        download_validator = download_validators.DownloadValidator(
            directory_path=directory_path)

        # Include retrying.
        stop_strategy = retry.stop_strategies.AfterDuration(
            maximum_duration=self._properties['download_validator']['policy']['stop_strategy']['maximum_duration'])
        wait_strategy = retry.wait_strategies.Fixed(
            wait_time=self._properties['download_validator']['policy']['wait_strategy']['wait_time'])
        logger = logging.getLogger(
            name=self._properties['download_validator']['policy']['messaging_broker']['logger']['name'])
        messaging_broker_factory = retry.messaging.broker_factories.Logging(
            logger=logger)
        messaging_broker = messaging_broker_factory.create(
            event_name='DOWNLOAD_VALIDATE')
        policy_builder = retry.PolicyBuilder() \
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

    def __init__(self, message_queue, properties):

        """
        Parameters
        ----------
        message_queue : Queue.Queue
        properties : collections.Mapping
        """

        self._factory = Factory(properties=properties)
        self._message_queue = message_queue
        self._properties = properties

    def create(self):
        # Construct the consumer.
        dependencies = self.create_dependencies()

        builder = messaging.consumer.builders.Builder() \
            .with_fetcher(dependencies['fetcher']) \
            .with_handler(dependencies['handler'])
        for filter in dependencies['filters']:
            builder = builder.with_filter(filter)
        consumer = builder.build()

        return consumer

    def create_dependencies(self):

        """
        Returns
        -------
        dict
        """

        dependencies = dict()

        # Construct the buffering fetcher.
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._properties['fetcher']['wait_time']['maximum'])
        fetcher = fetchers.BufferingFetcher(
            queue=self._message_queue,
            countdown_timer=countdown_timer,
            maximum_message_count=self._properties['fetcher']['message_count']['maximum'])
        dependencies['fetcher'] = fetcher

        # Construct the download handler.
        download_bot = self._factory.create()
        handler = handlers.Download(download_bot=download_bot)

        # Include orchestration.
        logger = logging.getLogger(
            name=self._properties['handler']['logger']['name'])
        handler = handlers.Orchestrating(handler=handler, logger=logger)
        dependencies['handler'] = handler

        # Construct the filters.
        dependencies['filters'] = list()

        # Construct the except generation seven metagame filter.
        except_generation_seven_metagame = filters.ExceptGenerationSevenMetagameFilter()
        dependencies['filters'].append(except_generation_seven_metagame)

        # Construct the except overused metagame filter.
        except_overused_metagame = filters.ExceptOverusedMetagameFilter()
        dependencies['filters'].append(except_overused_metagame)

        return dependencies

    def __repr__(self):
        repr_ = '{}(message_queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._message_queue,
                            self._properties)


class Nop(Consumer):

    def create_dependencies(self):
        dependencies = super(Nop, self).create_dependencies()

        # Construct the nop handler.
        handler = handlers.Nop()
        dependencies['handler'] = handler

        return dependencies
