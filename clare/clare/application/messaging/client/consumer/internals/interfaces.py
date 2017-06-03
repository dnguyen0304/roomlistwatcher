# -*- coding: utf-8 -*-

import abc


class IFilter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def filter(self, record):

        """
        Parameters
        ----------
        record : clare.application.messaging.client.records.Record

        Returns
        -------
        clare.application.messaging.client.records.Record
            If the record should not be filtered.
        None
            If the record should be filtered.
        """

        pass


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, record):

        """
        Parameters
        ----------
        record : clare.application.messaging.client.records.Record
        """

        pass
