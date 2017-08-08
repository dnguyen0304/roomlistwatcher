# -*- coding: utf-8 -*-

import abc


class ISender(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message

        Raises
        ------
        clare.common.messaging.producer.exceptions.SendTimeout
        """

        raise NotImplementedError


class ISource(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message

        Raises
        ------
        clare.common.messaging.producer.exceptions.EmitTimeout
        """

        raise NotImplementedError
