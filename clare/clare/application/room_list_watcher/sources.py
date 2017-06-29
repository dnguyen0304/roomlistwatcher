# -*- coding: utf-8 -*-

from clare.common import messaging


class Deque(messaging.producer.interfaces.ISource):

    def __init__(self, deque, record_factory):

        """
        Parameters
        ----------
        deque : collections.deque
        record_factory : clare.application.room_list_watcher.record_factories.RecordFactory
        """

        self._deque = deque
        self._record_factory = record_factory

    def emit(self):
        try:
            value = self._deque.popleft()
        except IndexError:
            raise messaging.exceptions.Timeout
        else:
            record = self._record_factory.create(value=value)
            return record

    def __repr__(self):
        repr_ = '{}(deque={}, record_factory={})'
        return repr_.format(self.__class__.__name__,
                            self._deque,
                            self._record_factory)
