# -*- coding: utf-8 -*-

import collections
import uuid

from clare.common import messaging


class QueueToQueue(messaging.interfaces.Queue):

    def __init__(self, queue, properties):

        """
        Parameters
        ----------
        queue : Queue.Queue
        properties : collections.Mapping
        """

        self._queue = queue
        self._properties = properties

    def send(self, message):
        self._queue.put(item=message)

    def receive(self):
        self._queue.get(timeout=self._properties['message.receive.wait.seconds'])

    def __repr__(self):
        repr_ = '{}(queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._queue,
                            self._properties)


class SqsFifoQueueToQueue(messaging.interfaces.Queue):

    def __init__(self, sqs_queue, properties):

        """
        Parameters
        ----------
        sqs_queue : Boto3 SQS Queue Resource
        properties : collections.Mapping
        """

        self._buffer = collections.deque()

        self._sqs_queue = sqs_queue
        self._properties = properties

        # This attribute applies only to FIFO queues. SQS message
        # groups are comparable to Kafka topic partitions.
        self._message_group_id = str(uuid.uuid4())

    def send(self, message):
        self._sqs_queue.send_message(MessageBody=message.body,
                                     MessageGroupId=self._message_group_id)

    def receive(self):
        try:
            message = self._buffer.popleft()
        except IndexError:
            # There was a cache miss.
            messages = self._sqs_queue.receive_messages(
                MaxNumberOfMessages=str(self._properties['message.receive.maximum.count']),
                WaitTimeSeconds=self._properties['message.receive.wait.seconds'])
            self._buffer.extend(messages)
            message = self._buffer.popleft()
        return message

    def __repr__(self):
        repr_ = '{}(sqs_queue={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._properties)
