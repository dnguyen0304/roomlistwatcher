# -*- coding: utf-8 -*-

import time

from . import timers


class CountdownTimerFactory(object):

    def create(self, duration, _get_now_in_seconds=None):

        """
        Parameters
        ----------
        duration : float
            The units are in seconds since the epoch.
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.

        Returns
        -------
        clare.common.utilities.timers.CountdownTimer
        """

        timer = timers.CountdownTimer(
            duration=duration,
            _get_now_in_seconds=_get_now_in_seconds or time.time)
        return timer
