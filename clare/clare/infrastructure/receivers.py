# -*- coding: utf-8 -*-

import collections

from clare.common.messaging import consumer


class Sqs(consumer.receivers.Buffering):

    BATCH_SIZE_MINIMUM_COUNT = 1

    def __init__(self,
                 sqs_queue,
                 batch_size_count,
                 wait_time_seconds,
                 message_factory,
                 _buffer=None):

        """
        Parameters
        ----------
        sqs_queue : Boto3 SQS Queue Resource
        batch_size_count : int
            Size of the batch. The units are in number of messages.
        wait_time_seconds : int
            Duration for which to wait. The units are in seconds.
        message_factory : clare.common.messaging.factories.Message
        """

        self._sqs_queue = sqs_queue
        self._original_batch_size_count = batch_size_count
        self._wait_time_seconds = wait_time_seconds
        self._message_factory = message_factory

        self._buffer = _buffer if _buffer is not None else collections.deque()

        self._current_batch_size_count = batch_size_count

    def receive(self):
        if not self._buffer:
            self._fill_buffer()
        try:
            message = self._buffer.popleft()
        except IndexError:
            message = 'The receive operation timed out.'
            raise consumer.exceptions.ReceiveTimeout(message)
        return message

    def _fill_buffer(self):
        messages = self._sqs_queue.receive_messages(
            MaxNumberOfMessages=self._current_batch_size_count,
            WaitTimeSeconds=self._wait_time_seconds)
        for message in messages:
            marshalled = self._message_factory.create(message.body)
            self._buffer.append(marshalled)

    def minimize_batch_size_count(self):
        self._current_batch_size_count = Sqs.BATCH_SIZE_MINIMUM_COUNT

    def restore_batch_size_count(self):
        self._current_batch_size_count = self._original_batch_size_count

    def __repr__(self):
        repr_ = ('{}('
                 'sqs_queue={}, '
                 'batch_size_count={}, '
                 'wait_time_seconds={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._original_batch_size_count,
                            self._wait_time_seconds,
                            self._message_factory)
