# -*- coding: utf-8 -*-

from clare.common import messaging


class Deque(messaging.producer.sources.Source):

    def __init__(self, deque, message_factory):

        """
        Parameters
        ----------
        deque : collections.deque
        message_factory : clare.common.messaging.factories.Message
        """

        self._deque = deque
        self._message_factory = message_factory

    def emit(self):
        try:
            value = self._deque.popleft()
        except IndexError:
            message = 'The source timed out.'
            raise messaging.producer.exceptions.EmitTimeout(message)
        else:
            message = self._message_factory.create(body=value)
            return message

    def __repr__(self):
        repr_ = '{}(deque={}, message_factory={})'
        return repr_.format(self.__class__.__name__,
                            self._deque,
                            self._message_factory)
