# -*- coding: utf-8 -*-

from . import continue_strategies
from .retry_policy import RetryPolicy


class RetryPolicyBuilder(object):

    def __init__(self,
                 stop_strategies=None,
                 wait_strategy=None,
                 continue_strategies=None,
                 handled_exceptions=None):

        """
        Retry policies should have at least 1 stop strategy and at
        least 1 wait strategy. A "successful" attempt is understood as
        one where an exception was not thrown within the callable.

        Parameters
        ----------
        stop_strategies : iterable of IStopStrategy
            Defaults to an empty list.
        wait_strategy : IWaitStrategy
            Defaults to None.
        continue_strategies : iterable of IContinueStrategy
            Continuing takes precedence over stopping after successful
            attempts. In other words, it "overrides" those cases.
            Defaults to an empty list.
        handled_exceptions : iterable of Exception
            Defaults to an empty tuple.
        """

        self._stop_strategies = stop_strategies or list()
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies or list()
        self._handled_exceptions = handled_exceptions or tuple()

    def with_stop_strategy(self, stop_strategy):
        self._stop_strategies.append(stop_strategy)
        return self

    def with_wait_strategy(self, wait_strategy):
        self._wait_strategy = wait_strategy
        return self

    def _with_continue_strategy(self, continue_strategy):
        self._continue_strategies.append(continue_strategy)
        return self

    def continue_on_exception(self, exception):
        self._handled_exceptions += (exception,)
        return self

    def continue_if_result(self, predicate):
        continue_strategy = continue_strategies.AfterResult(predicate=predicate)
        return self._with_continue_strategy(continue_strategy)

    def build(self):
        retry_policy = RetryPolicy(stop_strategies=self._stop_strategies,
                                   wait_strategy=self._wait_strategy,
                                   continue_strategies=self._continue_strategies,
                                   handled_exceptions=self._handled_exceptions)
        return retry_policy
