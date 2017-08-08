# -*- coding: utf-8 -*-

import abc


class Receiver(object):

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


class Buffering(Receiver):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def minimize_batch_size_count(self):

        """
        Update the configuration to receive the fewest number of
        messages possible in each batch.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def restore_batch_size_count(self):

        """
        Update the configuration to receive the originally set number of
        messages in each batch.
        """

        raise NotImplementedError
