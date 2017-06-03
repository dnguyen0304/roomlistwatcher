# -*- coding: utf-8 -*-

from .. import records


class Fetcher(object):

    def __init__(self, queue, value_deserializer):

        """
        Parameters
        ----------
        queue : Queue.Queue
        value_deserializer : clare.application.messaging.interfaces.IDeserializer
        """

        self._queue = queue
        self._value_deserializer = value_deserializer

    def pop(self, timeout):

        """
        Parameters
        ----------
        timeout : float

        Returns
        -------
        clare.application.messaging.client.records.Record
        """

        data = self._queue.get(timeout=timeout)
        record = records.Record(
            queue_name=data['queue_name'],
            timestamp=data['timestamp'],
            value=self._value_deserializer.deserialize(data=data['value']))
        return record

    def __repr__(self):
        repr_ = '{}(queue={}, value_deserializer={})'
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._value_deserializer)
