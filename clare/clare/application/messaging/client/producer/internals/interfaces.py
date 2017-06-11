# -*- coding: utf-8 -*-

import abc


class ISource(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self):

        """
        Returns
        -------
        collections.Iterable
        """

        pass
