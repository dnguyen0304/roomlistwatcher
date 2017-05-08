# -*- coding: utf-8 -*-

from . import interfaces


class Observable(interfaces.INotifyable):

    def __init__(self):
        self._observers = set()

    def register(self, observer):

        """
        Parameters
        ----------
        observer : clare.event_driven.interfaces.INotifyable
        """

        self._observers.add(observer)

    def notify(self, event):

        """
        Parameters
        ----------
        event : str
        """

        for observer in self._observers:
            observer.notify(event=event)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
