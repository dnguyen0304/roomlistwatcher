# -*- coding: utf-8 -*-

import abc


class IFlushStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : typing.Any

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        pass


class IScraper(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def scrape(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        collections.Sequence
        """

        pass

    @abc.abstractmethod
    def _initialize(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        None
        """

        pass

    @abc.abstractmethod
    def _extract(self):

        """
        Returns
        -------
        collections.Sequence
        """

        pass

    @abc.abstractmethod
    def dispose(self):
        pass
