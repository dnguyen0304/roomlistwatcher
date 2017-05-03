# -*- coding: utf-8 -*-

import time

from .attempt import Attempt


class RetryPolicy(object):

    def __init__(self,
                 stop_strategy,
                 wait_strategy,
                 handled_exceptions=tuple()):

        """
        Parameters
        ----------
        stop_strategy : IStopStrategy
        wait_strategy : IWaitStrategy
        handled_exceptions : collections.Iterable
            Defaults to an empty tuple.
        """

        self._stop_strategy = stop_strategy
        self._wait_strategy = wait_strategy
        self._handled_exceptions = handled_exceptions

    def execute(self, callable, _sleep=time.sleep):

        """
        Parameters
        ----------
        callable : collections.Callable
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        attempt = Attempt(number=0,
                          was_successful=None,
                          result=None,
                          exception=None,
                          first_attempt_start_time=time.time())

        while True:
            attempt_number = attempt.number + 1
            was_successful = False
            result = None
            exception = None

            if (attempt.was_successful or
                self._stop_strategy.should_stop(attempt=attempt)):
                    break
            try:
                result = callable()
            except self._handled_exceptions as e:
                exception = e
            else:
                was_successful = True

            attempt = Attempt(
                number=attempt_number,
                was_successful=was_successful,
                result=result,
                exception=exception,
                first_attempt_start_time=attempt.first_attempt_start_time)

            _sleep(self._wait_strategy.compute_wait_time(attempt=attempt))

        if attempt.was_successful:
            return attempt.result

    def __repr__(self):
        repr_ = '{}(stop_strategy={}, wait_strategy={}, handled_exceptions={})'
        return repr_.format(self.__class__.__name__,
                            self._stop_strategy,
                            self._wait_strategy,
                            self._handled_exceptions)
