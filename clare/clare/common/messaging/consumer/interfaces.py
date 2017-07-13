# -*- coding: utf-8 -*-

import abc


class IConsumer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def consume(self, interval, timeout):

        """
        Parameters
        ----------
        interval : float
            Rate of work. The units are in seconds.
        timeout : float
            Maximum duration to try fetching a new record. The units
            are in seconds.

        Returns
        -------
        None
        """

        raise NotImplementedError

    @abc.abstractmethod
    def _consume_once(self, timeout):

        """
        Parameters
        ----------
        timeout : float
            Maximum duration to try fetching a new record. The units
            are in seconds.

        Returns
        -------
        None

        Raises
        ------
        clare.common.messaging.consumer.exceptions.FetchTimeout
            If the fetcher times out before fetching the minimum fetch size.
        """

        raise NotImplementedError


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

        Raises
        ------
        clare.common.messaging.consumer.exceptions.FetchTimeout
        """

        raise NotImplementedError


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record
        """

        raise NotImplementedError
