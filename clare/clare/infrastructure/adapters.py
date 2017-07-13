# -*- coding: utf-8 -*-

import uuid

from . import interfaces


class QueueToQueue(interfaces.IQueue):

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


class SqsFifoQueueToQueue(interfaces.IQueue):

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
