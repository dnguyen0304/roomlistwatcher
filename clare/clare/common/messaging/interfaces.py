# -*- coding: utf-8 -*-

import abc

from . import consumer
from . import producer


class IFilter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def filter(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message

        Returns
        -------
        clare.common.messaging.models.Message
            If the message should not be filtered.
        None
            If the message should be filtered.
        """

        pass


class Queue(producer.interfaces.ISender):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def receive(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message

        Raises
        ------
        clare.common.messaging.consumer.ReceiveTimeout
            If there weren't any buffered messages and the operation
            took too long to receive the configured number of messages.
        """

        raise NotImplementedError
