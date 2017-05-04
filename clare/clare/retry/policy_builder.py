# -*- coding: utf-8 -*-

from . import continue_strategies
from .policy import Policy


class PolicyBuilder(object):

    def __init__(self,
                 stop_strategies=None,
                 wait_strategy=None,
                 continue_strategies=None,
                 handled_exceptions=None,
                 pre_hooks=None,
                 post_hooks=None):

        """
        Policies must have the following:
          - exactly 1 wait strategy
        Policies should have the following:
          - at least 1 stop strategy
        Policies may have the following:
          - 0 or more exceptions on which to continue
          - 0 or more results on which to continue
          - 0 or more pre-hooks
          - 0 or more post-hooks

        A "successful" attempt is understood as one where an exception
        was not thrown within the callable.

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
        pre_hooks : iterable of callable
            See the method docstring for more details. Defaults to an
            empty list.
        post_hooks : iterable of callable
            See the method docstring for more details. Defaults to an
            empty list.
        """

        self._stop_strategies = stop_strategies or list()
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies or list()
        self._handled_exceptions = handled_exceptions or tuple()
        self._pre_hooks = pre_hooks or list()
        self._post_hooks = post_hooks or list()

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

    def add_pre_hook(self, pre_hook):

        """
        Register a callable to be executed before each attempt,
        including just before the algorithm stops.

        The hook receives a context object containing metadata about
        the current attempt number ("attempt_number").

        These hooks are read-only and therefore cannot affect the
        runtime behavior of the Policy.

        Parameters
        ----------
        pre_hook : callable
            The callable must accept one argument of type Mapping.
        """

        self._pre_hooks.append(pre_hook)
        return self

    def add_post_hook(self, post_hook):

        """
        Register a callable to be executed after each attempt.

        The hook receives a context object containing metadata about
        the returned result ("result"), the thrown exception
        ("exception"), and the next wait time ("next_wait_time").

        These hooks are read-only and therefore cannot affect the
        runtime behavior of the Policy.

        Parameters
        ----------
        post_hook : callable
            The callable must accept one argument of type Mapping.
        """

        self._post_hooks.append(post_hook)
        return self

    def build(self):
        retry_policy = Policy(stop_strategies=self._stop_strategies,
                              wait_strategy=self._wait_strategy,
                              continue_strategies=self._continue_strategies,
                              handled_exceptions=self._handled_exceptions,
                              pre_hooks=self._pre_hooks,
                              post_hooks=self._post_hooks)
        return retry_policy
