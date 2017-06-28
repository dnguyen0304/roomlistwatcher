# -*- coding: utf-8 -*-

from __future__ import print_function

import collections

from . import exceptions
from .topic import Topic
from clare import common
from clare.common import messaging
from clare.common import retry


class Download(messaging.consumer.interfaces.IHandler):

    def __init__(self, download_bot):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        """

        self._download_bot = download_bot

    def handle(self, record):
        url = record.value
        file_path = self._download_bot.run(url=url)
        return file_path

    def __repr__(self):
        repr_ = '{}(download_bot={})'
        return repr_.format(self.__class__.__name__, self._download_bot)


class Nop(messaging.consumer.interfaces.IHandler):

    def handle(self, record):

        """
        Returns
        -------
        None
        """

        pass

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class Orchestrating(messaging.consumer.interfaces.IHandler):

    def __init__(self, handler, logger):

        """
        Parameters
        ----------
        handler : clare.application.download_bot.handlers.Download
        logger : logging.Logger
        """

        self._handler = handler
        self._logger = logger

    def handle(self, record):
        try:
            file_path = self._handler.handle(record=record)
        except (exceptions.RoomExpired, retry.exceptions.MaximumRetry) as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.debug(msg=message)
        else:
            arguments = collections.OrderedDict()
            arguments['file_path'] = file_path
            event = common.logging.Event(topic=Topic.REPLAY_DOWNLOADED,
                                         arguments=arguments)
            self._logger.info(msg=event.to_json())

    def __repr__(self):
        repr_ = '{}(handler={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._handler,
                            self._logger)


class Printing(messaging.consumer.interfaces.IHandler):

    def __init__(self, handler):

        """
        Parameters
        ----------
        handler : clare.application.download_bot.handlers.Download
        """

        self._handler = handler

    def handle(self, record):
        file_path = self._handler.handle(record=record)
        print(file_path)

    def __repr__(self):
        repr_ = '{}(handler={})'
        return repr_.format(self.__class__.__name__, self._handler)
