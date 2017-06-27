# -*- coding: utf-8 -*-

import abc


class IScraper(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self, url):

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
