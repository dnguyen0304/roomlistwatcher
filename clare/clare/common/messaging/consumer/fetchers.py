# -*- coding: utf-8 -*-

from . import interfaces


class Fetcher(interfaces.IFetcher):

    def __init__(self, message_queue):

        """
        Parameters
        ----------
        message_queue : Queue.Queue
        """

        self._message_queue = message_queue

    def pop(self, timeout):
        record = self._message_queue.get(timeout=timeout)
        return record

    def __repr__(self):
        repr_ = '{}(message_queue={})'
        return repr_.format(self.__class__.__name__, self._message_queue)
