# -*- coding: utf-8 -*-

from .observable import Observable


class ObservableFactory(object):

    def build(self):

        """
        Returns
        ----------
        clare.event_driven.interfaces.INotifyable
        """

        observable = Observable()
        return observable
