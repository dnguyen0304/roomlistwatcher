# -*- coding: utf-8 -*-

import time

from . import timers


class CountdownTimerFactory(object):

    def __init__(self, _get_now_in_seconds=None):

        """
        Parameters
        ----------
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        """

        self._get_now_in_seconds = _get_now_in_seconds or time.time

    def create(self, duration):

        """
        Parameters
        ----------
        duration : float
            The units are in seconds since the epoch.

        Returns
        -------
        clare.common.utilities.timers.CountdownTimer
        """

        timer = timers.CountdownTimer(
            duration=duration,
            _get_now_in_seconds=self._get_now_in_seconds)
        return timer

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
