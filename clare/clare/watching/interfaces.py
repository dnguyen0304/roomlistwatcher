# -*- coding: utf-8 -*-

import abc


class IFilterStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_filter(self, path):

        """
        Parameters
        ----------
        path : str

        Returns
        -------
        bool
            True if the path should be filtered.
        """

        pass
