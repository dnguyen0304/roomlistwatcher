# -*- coding: utf-8 -*-

import time

from . import interfaces
from clare import common


class AfterDuration(interfaces.IFlushStrategy):

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
            should_flush = common.utilities.should_stop(
                maximum_duration=self._maximum_duration,
                start_time=self._start_time,
                _get_now_in_seconds=self._get_now_in_seconds)
        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_duration={})'
        return repr_.format(self.__class__.__name__, self._maximum_duration)


class AfterSize(interfaces.IFlushStrategy):

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
