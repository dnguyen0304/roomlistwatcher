# -*- coding: utf-8 -*-

import abc


class StringFilter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def filter(self, data):

        """
        Parameters
        ----------
        data : str

        Returns
        -------
        str
            If the data should not be filtered.
        None
            If the data should be filtered.
        """

        pass
