# -*- coding: utf-8 -*-

import collections

from clare.common.messaging import consumer

BATCH_SIZE_MINIMUM_COUNT = 1


class Queue(consumer.receivers.Buffering):

    def __init__(self,
                 batch_size_maximum_count,
                 countdown_timer,
                 message_factory,
                 batch_size_minimum_count=BATCH_SIZE_MINIMUM_COUNT,
                 _queue=None,
                 _buffer=None):

        """
        Parameters
        ----------
        batch_size_maximum_count : int
            Maximum size of the batch. The units are in number of
            messages.
        batch_size_minimum_count : int
            Minimum size of the batch. The units are in number of
            messages. Defaults to BATCH_SIZE_MINIMUM_COUNT.
        countdown_timer : clare.common.utilities.timers.CountdownTimer
        message_factory : clare.common.messaging.factories.Message
        """

        self._original_batch_size_maximum_count = batch_size_maximum_count
        self._original_batch_size_minimum_count = batch_size_minimum_count
        self._countdown_timer = countdown_timer
        self._message_factory = message_factory

        # Deques are thread-safe.
        self._queue = _queue if _queue is not None else collections.deque()
        self._buffer = _buffer if _buffer is not None else collections.deque()

        self._current_batch_size_maximum_count = batch_size_maximum_count
        self._current_batch_size_minimum_count = batch_size_minimum_count

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
        messages = list()

        self._countdown_timer.start()

        while True:
            # This must run at least once (i.e. do-while semantics).
            try:
                message = self._queue.popleft()
            except IndexError:
                pass
            else:
                messages.append(message)

            if len(messages) == self._current_batch_size_maximum_count:
                break
            if not self._countdown_timer.has_time_remaining:
                break

        self._countdown_timer.reset()

        if len(messages) < self._current_batch_size_minimum_count:
            # Return the messages to the queue.
            # Use extendleft alongside reversed to maintain the order.
            self._queue.extendleft(reversed(messages))
        else:
            # Add the marshalled messages to the buffer.
            marshalled = (self._message_factory.create(message.body)
                          for message
                          in messages)
            self._buffer.extend(marshalled)

    def minimize_batch_size_count(self):
        self._current_batch_size_maximum_count = self._original_batch_size_minimum_count

    def restore_batch_size_count(self):
        self._current_batch_size_maximum_count = self._original_batch_size_maximum_count

    def __repr__(self):
        repr_ = ('{}('
                 'batch_size_maximum_count={}, '
                 'batch_size_minimum_count={}, '
                 'countdown_timer={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._original_batch_size_maximum_count,
                            self._original_batch_size_minimum_count,
                            self._countdown_timer,
                            self._message_factory)


class Sqs(consumer.receivers.Buffering):

    def __init__(self,
                 sqs_queue,
                 batch_size_maximum_count,
                 wait_time_seconds,
                 message_factory,
                 batch_size_minimum_count=BATCH_SIZE_MINIMUM_COUNT,
                 _buffer=None):

        """
        Parameters
        ----------
        sqs_queue : Boto3 SQS Queue Resource
        batch_size_maximum_count : int
            Maximum size of the batch. The units are in number of
            messages.
        batch_size_minimum_count : int
            Minimum size of the batch. The units are in number of
            messages. Defaults to BATCH_SIZE_MINIMUM_COUNT.
        wait_time_seconds : int
            Duration for which to wait. The units are in seconds.
        message_factory : clare.common.messaging.factories.Message
        """

        self._sqs_queue = sqs_queue
        self._original_batch_size_maximum_count = batch_size_maximum_count
        self._original_batch_size_minimum_count = batch_size_minimum_count
        self._wait_time_seconds = wait_time_seconds
        self._message_factory = message_factory

        self._buffer = _buffer if _buffer is not None else collections.deque()

        self._current_batch_size_maximum_count = batch_size_maximum_count

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
            MaxNumberOfMessages=self._current_batch_size_maximum_count,
            WaitTimeSeconds=self._wait_time_seconds)
        for message in messages:
            marshalled = self._message_factory.create(message.body)
            self._buffer.append(marshalled)

    def minimize_batch_size_count(self):
        self._current_batch_size_maximum_count = self._original_batch_size_minimum_count

    def restore_batch_size_count(self):
        self._current_batch_size_maximum_count = self._original_batch_size_maximum_count

    def __repr__(self):
        repr_ = ('{}('
                 'sqs_queue={}, '
                 'batch_size_maximum_count={}, '
                 'batch_size_minimum_count={}, '
                 'wait_time_seconds={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._original_batch_size_maximum_count,
                            self._original_batch_size_minimum_count,
                            self._wait_time_seconds,
                            self._message_factory)
