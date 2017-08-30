# -*- coding: utf-8 -*-

import collections

from . import topics
from room_list_watcher.common import messaging


class Logging(messaging.producing.senders.Sender):

    def __init__(self, sender, logger):

        """
        Parameters
        ----------
        sender : room_list_watcher.common.messaging.producing.senders.Sender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def send(self, data):
        self._sender.send(data=data)

        arguments = collections.OrderedDict()
        arguments['path'] = data
        event = messaging.events.StructuredEvent(topic=topics.Topic.ROOM_FOUND,
                                                 arguments=arguments)
        message = event.to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
