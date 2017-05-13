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


class IElementLookup(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_by_css_selector(self, css_selector):

        """
        Parameters
        ----------
        css_selector : str
            Equivalent to the CSS selector $("<css_selector>").

        Returns
        -------
        collections.Sequence
        """

        pass

    @abc.abstractmethod
    def find_by_class_name(self, class_name):

        """
        Parameters
        ----------
        class_name : str
            Equivalent to the CSS selector $(".<class_name>").

        Returns
        -------
        collections.Sequence
        """

        pass
