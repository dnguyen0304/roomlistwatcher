# -*- coding: utf-8 -*-


class QueueClient(object):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def calculate_message_count(self):

        """
        Get the approximate number of messages in the queue.

        The result is unreliable because the consistency guarantees are
        not sufficient.

        Returns
        -------
        int
        """

        message_count = self._queue.qsize()
        return message_count

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)
