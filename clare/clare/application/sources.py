# -*- coding: utf-8 -*-

import sys
import threading

if sys.version_info[:2] == (2, 7):
    import Queue as queue

from .messaging.client import producer


class Batched(producer.internals.interfaces.ISource):

    def __init__(self, worker_thread, message_queue):

        """
        Parameters
        ----------
        worker_thread : threading.Thread
        message_queue : Queue.Queue
        """

        self._worker_thread = worker_thread
        self._message_queue = message_queue

    def emit(self):

        """
        Returns
        -------
        collections.Iterable
        """

        if not self._worker_thread.is_alive():
            self._worker_thread.daemon = True
            self._worker_thread.start()

        records = list()

        while True:
            try:
                records.append(self._message_queue.get(block=False))
            except queue.Empty:
                break

        return records

    def __repr__(self):
        repr_ = '{}(worker_thread={}, message_queue={})'
        return repr_.format(self.__class__.__name__,
                            self._worker_thread,
                            self._message_queue)
