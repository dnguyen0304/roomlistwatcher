# -*- coding: utf-8 -*-

import abc


class IDisposable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self):
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

        Raises
        ------
        clare.scraping.exceptions.HttpError
        clare.watching.scraping.exceptions.ExtractFailed
        """

        pass
