# -*- coding: utf-8 -*-

from ...common import messaging


class Deque(messaging.producer.sources.Source):

    def __init__(self, deque):

        """
        Parameters
        ----------
        deque : collections.deque
        """

        self._deque = deque

    def emit(self):
        try:
            data = self._deque.popleft()
        except IndexError:
            message = 'The source timed out.'
            raise messaging.producer.exceptions.EmitTimeout(message)
        else:
            return data

    def __repr__(self):
        repr_ = '{}(deque={})'
        return repr_.format(self.__class__.__name__, self._deque)
