# -*- coding: utf-8 -*-

import abc


class IDisposable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self):
        pass


class IExtractStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def extract(self, url):

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
