# -*- coding: utf-8 -*-

import abc


class IDownloadStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def download(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Download unique identifier.

        Raises
        ------
        clare.scraper.download_strategies.HttpError
            If the server returned an error.
        clare.scraper.download_strategies.DownloadFailed
            If the room expired.
        """

        pass
