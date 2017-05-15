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
        clare.scraping.exceptions.DownloadFailed
            If the room expired.
        clare.scraping.exceptions.HttpError
            If the server returned an error.
        """

        pass
