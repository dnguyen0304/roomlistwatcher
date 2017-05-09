# -*- coding: utf-8 -*-

import abc


class DownloadFailed(Exception):
    pass


class IDownloadStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Path to the downloaded file.
        """

        pass

    def dispose(self):
        pass


class Fail(IDownloadStrategy):

    def execute(self, url):

        """
        Raises
        ------
        clare.crawler.download_strategies.DownloadFailed
        """

        raise DownloadFailed

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
