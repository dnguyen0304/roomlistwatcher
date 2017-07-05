# -*- coding: utf-8 -*-


class InotifyToIterableAdapter(object):

    def __init__(self, inotify):

        """
        Parameters
        ----------
        inotify : inotify.adapters.Inotify
        """

        self._inotify = inotify

    def next(self):

        """
        Returns
        -------
        tuple
        """

        event = next(self._inotify.event_gen())
        return event

    def __iter__(self):
        return self

    def __repr__(self):
        repr_ = '{}(inotify={})'
        return repr_.format(self.__class__.__name__, self._inotify)
