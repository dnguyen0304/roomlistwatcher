# -*- coding: utf-8 -*-

import time

from .attempt import Attempt


class RetryPolicy(object):

    def __init__(self,
                 stop_strategies,
                 wait_strategy,
                 continue_strategies,
                 handled_exceptions,
                 pre_hooks,
                 post_hooks):
        self._stop_strategies = stop_strategies
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies
        self._handled_exceptions = handled_exceptions
        self._pre_hooks = pre_hooks
        self._post_hooks = post_hooks

    def execute(self, callable, _sleep=time.sleep):

        """
        Parameters
        ----------
        callable : callable
        _sleep : callable
            Used internally. Defaults to time.sleep.
        """

        attempt = Attempt(number=0,
                          was_successful=None,
                          result=None,
                          exception=None,
                          first_attempt_start_time=time.time())

        while True:
            attempt_number = attempt.number + 1
            was_successful = None
            result = None
            exception = None

            should_stop = any(
                stop_strategy.should_stop(attempt=attempt)
                for stop_strategy
                in self._stop_strategies)
            should_continue = any(
                continue_strategy.should_continue(attempt=attempt)
                for continue_strategy
                in self._continue_strategies)

            self._call_pre_hooks(attempt_number=attempt_number,
                                 was_successful=attempt.was_successful,
                                 should_stop=should_stop,
                                 should_continue=should_continue)

            if should_stop or (attempt.was_successful and not should_continue):
                break
            else:
                try:
                    result = callable()
                except self._handled_exceptions as e:
                    was_successful = False
                    exception = e
                else:
                    was_successful = True

            attempt = Attempt(
                number=attempt_number,
                was_successful=was_successful,
                result=result,
                exception=exception,
                first_attempt_start_time=attempt.first_attempt_start_time)

            wait_time = self._wait_strategy.compute_wait_time(attempt=attempt)

            self._call_post_hooks(result=result,
                                  exception=exception,
                                  wait_time=wait_time)
            _sleep(wait_time)

        if attempt.was_successful:
            return attempt.result

    def _call_pre_hooks(self,
                        attempt_number,
                        was_successful,
                        should_stop,
                        should_continue):
        context = {'attempt_number': attempt_number,
                   'was_successful': was_successful,
                   'should_stop': should_stop,
                   'should_continue': should_continue}
        for pre_hook in self._pre_hooks:
            pre_hook(context)

    def _call_post_hooks(self, result, exception, wait_time):
        context = {'result': result,
                   'exception': exception,
                   'next_wait_time': wait_time}
        for post_hook in self._post_hooks:
            post_hook(context)

    def __repr__(self):
        repr_ = ('{}('
                 'stop_strategies={}, '
                 'wait_strategy={}, '
                 'continue_strategies={}, '
                 'handled_exceptions={}, '
                 'pre_hooks={}, '
                 'post_hooks={})')
        return repr_.format(self.__class__.__name__,
                            self._stop_strategies,
                            self._wait_strategy,
                            self._continue_strategies,
                            self._handled_exceptions,
                            self._pre_hooks,
                            self._post_hooks)
