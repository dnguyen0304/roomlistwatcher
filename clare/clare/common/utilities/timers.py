# -*- coding: utf-8 -*-

import time


class CountdownTimer(object):

    def __init__(self, duration, _get_now_in_seconds=None):

        """
        Parameters
        ----------
        duration : float
            The units are in seconds since the epoch.
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        """

        self._duration = duration
        self._get_now_in_seconds = _get_now_in_seconds or time.time

        self.start_time = None

    def start(self):
        self.start_time = self._get_now_in_seconds()

    def should_stop(self):

        """
        Returns
        -------
        bool
            True if the process should stop.
        """

        now = self._get_now_in_seconds()
        current_duration = now - self.start_time
        if current_duration >= self._duration:
            result = True
        else:
            result = False

        return result

    def __repr__(self):
        repr_ = '{}(duration={})'
        return repr_.format(self.__class__.__name__, self._duration)
