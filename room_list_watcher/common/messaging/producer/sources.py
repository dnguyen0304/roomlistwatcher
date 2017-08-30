# -*- coding: utf-8 -*-

import abc


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
