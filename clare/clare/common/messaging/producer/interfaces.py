# -*- coding: utf-8 -*-

import abc


class ISource(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self):

        """
        Returns
        -------
        clare.common.messaging.record.Record
        """

        pass
