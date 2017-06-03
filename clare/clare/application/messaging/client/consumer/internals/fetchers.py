# -*- coding: utf-8 -*-

from clare.application.messaging.client import records


class Fetcher(object):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

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
        record = records.Record(queue_name=data['queue_name'],
                                timestamp=data['timestamp'],
                                value=data['value'])
        return record

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)
