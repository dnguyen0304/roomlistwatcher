# -*- coding: utf-8 -*-

import abc


class Notifyable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, event):

        """
        Parameters
        ----------
        event : str

        Returns
        ------
        None
        """

        pass
