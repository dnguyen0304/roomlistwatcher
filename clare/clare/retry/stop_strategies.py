# -*- coding: utf-8 -*-

import abc


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


class AfterAttempt(IStopStrategy):

    def __init__(self, maximum_attempt):
        self._maximum_attempt = maximum_attempt

    def should_stop(self, attempt):
        return (attempt.was_successful or
                attempt.number >= self._maximum_attempt)

    def __repr__(self):
        repr_ = '{}(maximum_attempt={})'
        return repr_.format(self.__class__.__name__, self._maximum_attempt)
