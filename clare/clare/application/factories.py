# -*- coding: utf-8 -*-

import sys
import threading

if sys.version_info[:2] == (2, 7):
    import Queue as queue

from . import applications
from . import download_bot
from . import room_list_watcher
from clare.common import messaging


class Factory(object):

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
        clare.application.applications.Application
        """

        message_queue = queue.Queue()

        # Construct the room_list_watcher.
        sender = messaging.producer.senders.Sender(
            message_queue=message_queue)
        room_list_watcher_factory = room_list_watcher.factories.Producer(
            properties=self._properties['room_list_watcher'],
            sender=sender)
        room_list_watcher_ = room_list_watcher_factory.create()

        # Include threading.
        kwargs = {
            'interval': self._properties['room_list_watcher']['interval'],
            'timeout': self._properties['room_list_watcher']['timeout']
        }
        room_list_watcher_ = threading.Thread(name='room_list_watcher',
                                              target=room_list_watcher_.produce,
                                              kwargs=kwargs)
        room_list_watcher_.daemon = True

        # Construct the download_bot.
        fetcher = messaging.consumer.fetchers.Fetcher(
            message_queue=message_queue)
        download_bot_factory = download_bot.factories.Consumer(
            properties=self._properties['download_bot'],
            fetcher=fetcher)
        download_bot_ = download_bot_factory.create()

        # Include threading.
        kwargs = {
            'interval': self._properties['download_bot']['interval'],
            'timeout': self._properties['download_bot']['timeout']
        }
        download_bot_ = threading.Thread(name='download_bot',
                                         target=download_bot_.consume,
                                         kwargs=kwargs)
        download_bot_.daemon = True

        # Construct the application.
        application = applications.Application(
            room_list_watcher=room_list_watcher_,
            download_bot=download_bot_)

        return application

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
