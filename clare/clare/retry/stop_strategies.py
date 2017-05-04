# -*- coding: utf-8 -*-

import abc
import time


class IStopStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_stop(self, attempt):

        """
        Parameters
        ----------
        attempt : Attempt

        Returns
        -------
        bool
            True if the client should stop and False otherwise.
        """

        pass


class After(IStopStrategy):

    __metaclass__ = abc.ABCMeta

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class AfterAttempt(After):

    def __init__(self, maximum_attempt):
        self._maximum_attempt = maximum_attempt

    def should_stop(self, attempt):
        return attempt.number >= self._maximum_attempt

    def __repr__(self):
        repr_ = '{}(maximum_attempt={})'
        return repr_.format(self.__class__.__name__, self._maximum_attempt)


class AfterDuration(After):

    def __init__(self, maximum_duration, _get_now_in_seconds=time.time):

        """
        Parameters
        ----------
        maximum_duration : float
            The units are in seconds.
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        """

        self._maximum_duration = maximum_duration
        self._get_now_in_seconds = _get_now_in_seconds

    def should_stop(self, attempt):

        # Stopping the execution of callable where a single attempt
        # takes longer than the maximum duration is not supported.
        now = self._get_now_in_seconds()
        current_duration = now - attempt.first_attempt_start_time
        result = current_duration >= self._maximum_duration

        return result

    def __repr__(self):
        repr_ = '{}(maximum_duration={}, _get_now_in_seconds={})'
        return repr_.format(self.__class__.__name__,
                            self._maximum_duration,
                            self._get_now_in_seconds)


class AfterNever(After):

    def should_stop(self, attempt):
        return False
