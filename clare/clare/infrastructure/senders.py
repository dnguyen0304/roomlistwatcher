# -*- coding: utf-8 -*-

import httplib
import uuid

from clare.common.messaging import producer


class ConcurrentLinkedDeque(producer.senders.Sender):

    def __init__(self, deque):

        """
        Parameters
        ----------
        deque : collections.deque
        """

        self._deque = deque

    def send(self, message):
        self._deque.append(message)

    def __repr__(self):
        repr_ = '{}(deque={})'
        return repr_.format(self.__class__.__name__, self._deque)


class SqsFifoQueue(producer.senders.Sender):

    def __init__(self, sqs_queue, _message_group_id=None):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

        # This attribute applies only to FIFO queues. SQS message
        # groups are comparable to Kafka topic partitions.
        self._message_group_id = (_message_group_id
                                  if _message_group_id is not None
                                  else str(uuid.uuid4()))

    def send(self, message):
        response = self._sqs_queue.send_message(
            MessageBody=message.body,
            MessageGroupId=self._message_group_id)
        if response['ResponseMetadata']['HTTPStatusCode'] != httplib.OK:
            raise producer.exceptions.SendTimeout(str(response))

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)
