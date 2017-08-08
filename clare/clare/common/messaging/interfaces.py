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


class Queue(producer.interfaces.ISender, consumer.interfaces.Receiver):

    __metaclass__ = abc.ABCMeta
