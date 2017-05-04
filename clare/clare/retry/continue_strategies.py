# -*- coding: utf-8 -*-

import abc


class IContinueStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_continue(self, attempt):

        """
        Parameters
        ----------
        attempt : Attempt

        Returns
        -------
        bool
            True if the client should continue and False otherwise.
        """

        pass


class AfterResult(IContinueStrategy):

    def __init__(self, predicate):

        """
        Parameters
        ----------
        predicate : callable
            The callable must accept one argument and should return a
            boolean.
        """

        self._predicate = predicate

    def should_continue(self, attempt):
        result = self._predicate(attempt.result)
        return result

    def __repr__(self):
        repr_ = '{}(predicate={})'
        return repr_.format(self.__class__.__name__, self._predicate)
