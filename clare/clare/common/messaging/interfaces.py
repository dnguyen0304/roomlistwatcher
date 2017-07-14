# -*- coding: utf-8 -*-

import abc


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
