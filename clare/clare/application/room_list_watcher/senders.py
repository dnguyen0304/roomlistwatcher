# -*- coding: utf-8 -*-

import collections

from . import topics
from clare import common
from clare.common import messaging


class Logging(messaging.producer.interfaces.ISender):

    def __init__(self, sender, logger):

        """
        Parameters
        ----------
        sender : clare.common.messaging.producer.interfaces.ISender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def send(self, message):
        self._sender.send(message=message)

        arguments = collections.OrderedDict()
        arguments['path'] = message.body
        event = common.logging.Event(topic=topics.Topic.ROOM_FOUND,
                                     arguments=arguments)
        message = event.to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
