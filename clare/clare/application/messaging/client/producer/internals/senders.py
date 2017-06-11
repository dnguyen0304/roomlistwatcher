# -*- coding: utf-8 -*-


class Sender(object):

    def __init__(self, message_queue):

        """
        Parameters
        ----------
        message_queue : Queue.Queue
        """

        self._message_queue = message_queue

    def push(self, record, timeout):

        """
        Parameters
        ----------
        record : clare.application.messaging.client.records.Record
        timeout : float
        """

        self._message_queue.put(item=record, timeout=timeout)

    def __repr__(self):
        repr_ = '{}(message_queue={})'
        return repr_.format(self.__class__.__name__, self._message_queue)
