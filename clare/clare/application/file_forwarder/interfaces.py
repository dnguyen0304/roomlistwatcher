# -*- coding: utf-8 -*-

import abc


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, event):

        """
        Parameters
        ----------
        event : tuple

        Returns
        -------
        None
        """

        pass
