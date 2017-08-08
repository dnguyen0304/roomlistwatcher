# -*- coding: utf-8 -*-

from clare.common.messaging import producer


class Queue(producer.senders.Sender):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def send(self, message):
        self._queue.put(item=message)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)
