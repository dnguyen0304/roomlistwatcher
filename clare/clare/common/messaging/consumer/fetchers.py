# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

from . import exceptions
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
        try:
            record = self._message_queue.get(timeout=timeout)
        except queue.Empty:
            message = 'The fetcher timed out after {timeout} seconds.'
            raise exceptions.FetchTimeout(message.format(timeout=timeout))
        return record

    def __repr__(self):
        repr_ = '{}(message_queue={})'
        return repr_.format(self.__class__.__name__, self._message_queue)
