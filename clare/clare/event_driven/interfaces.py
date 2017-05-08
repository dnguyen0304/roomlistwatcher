# -*- coding: utf-8 -*-

import abc


class INotifyable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, event):

        """
        Parameters
        ----------
        event : clare.retry.policy.IJsonSerializable

        Returns
        ------
        None
        """

        pass
