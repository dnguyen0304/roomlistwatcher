# -*- coding: utf-8 -*-

import abc


class INotifyable(object):

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
