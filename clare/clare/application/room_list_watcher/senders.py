# -*- coding: utf-8 -*-

import collections

from . import topics
from clare import common


class Logging(object):

    def __init__(self, sender, logger):

        """
        Parameters
        ----------
        sender : clare.common.messaging.producer.senders.Sender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def push(self, record, timeout):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record
        timeout : float
        """

        self._sender.push(record=record, timeout=timeout)

        arguments = collections.OrderedDict()
        arguments['path'] = record.value
        event = common.logging.Event(topic=topics.Topic.ROOM_FOUND,
                                     arguments=arguments)
        message = event.to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
