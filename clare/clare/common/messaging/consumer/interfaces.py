# -*- coding: utf-8 -*-

import abc


class IFetcher(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def pop(self, timeout):

        """
        Parameters
        ----------
        timeout : float

        Returns
        -------
        clare.common.messaging.records.Record
        """

        pass


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record
        """

        pass
