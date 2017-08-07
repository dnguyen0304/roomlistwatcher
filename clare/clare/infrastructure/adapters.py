# -*- coding: utf-8 -*-

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

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : Boto3 SQS Queue Resource
        """

        self._sqs_queue = sqs_queue

        # This attribute applies only to FIFO queues. SQS message
        # groups are comparable to Kafka topic partitions.
        self._message_group_id = str(uuid.uuid4())

    def send(self, message):
        self._sqs_queue.send_message(MessageBody=message.body,
                                     MessageGroupId=self._message_group_id)

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
