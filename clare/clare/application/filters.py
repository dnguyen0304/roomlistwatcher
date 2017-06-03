# -*- coding: utf-8 -*-

import time


class _AfterDuration(object):

    def __init__(self, maximum_duration, _get_now_in_seconds=None):

        """
        Parameters
        ----------
        maximum_duration : float
            Maximum duration in seconds.
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        """

        self._maximum_duration = maximum_duration
        self._get_now_in_seconds = _get_now_in_seconds or time.time
        self._start_time = 0.0

    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : typing.Any

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        if not self._start_time:
            self._start_time = self._get_now_in_seconds()
            should_flush = False
        else:
            now = self._get_now_in_seconds()
            current_duration = now - self._start_time
            if current_duration >= self._maximum_duration:
                should_flush = True
            else:
                should_flush = False
        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_duration={})'
        return repr_.format(self.__class__.__name__, self._maximum_duration)


class _AfterSize(object):

    def __init__(self, maximum_size):

        """
        Parameters
        ----------
        maximum_size : int
        """

        self._maximum_size = maximum_size

    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : collections.Sized

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        if len(collection) >= self._maximum_size:
            should_flush = True
        else:
            should_flush = False
        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_size={})'
        return repr_.format(self.__class__.__name__, self._maximum_size)
