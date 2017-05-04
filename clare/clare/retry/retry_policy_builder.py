# -*- coding: utf-8 -*-

from . import stop_strategies
from .retry_policy import RetryPolicy


class RetryPolicyBuilder(object):

    def __init__(self,
                 stop_strategies=None,
                 wait_strategy=None,
                 handled_exceptions=None):

        """
        Retry policies should have at least 1 stop strategy and at
        least 1 wait strategy.

        Parameters
        ----------
        stop_strategies : iterable of IStopStrategy
            Defaults to an empty list.
        wait_strategy : IWaitStrategy
            Defaults to None.
        handled_exceptions : iterable of Exception
            Defaults to an empty tuple.
        """

        self._stop_strategies = stop_strategies
        self._wait_strategy = wait_strategy
        self._handled_exceptions = handled_exceptions

    def with_stop_strategy(self, stop_strategy):
        if not self._stop_strategies:
            self._stop_strategies = list()
            self._stop_strategies.append(stop_strategies.AfterSuccess())
        self._stop_strategies.append(stop_strategy)
        return self

    def with_wait_strategy(self, wait_strategy):
        self._wait_strategy = wait_strategy
        return self

    def continue_on_exception(self, exception):
        if not self._handled_exceptions:
            self._handled_exceptions = tuple()
        self._handled_exceptions += (exception,)
        return self

    def build(self):
        retry_policy = RetryPolicy(stop_strategies=self._stop_strategies,
                                   wait_strategy=self._wait_strategy,
                                   handled_exceptions=self._handled_exceptions)
        return retry_policy
