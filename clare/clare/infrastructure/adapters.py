# -*- coding: utf-8 -*-

import uuid

from clare.common.messaging import producer


class SqsFifoQueueToQueue(producer.senders.Sender):

    def __init__(self, sqs_queue, receiver):

        """
        Parameters
        ----------
        sqs_queue : Boto3 SQS Queue Resource
        receiver : clare.infrastructure.receivers.SqsReceiver
        """

        self._sqs_queue = sqs_queue
        self._receiver = receiver

        # This attribute applies only to FIFO queues. SQS message
        # groups are comparable to Kafka topic partitions.
        self._message_group_id = str(uuid.uuid4())

    def send(self, message):
        self._sqs_queue.send_message(MessageBody=message.body,
                                     MessageGroupId=self._message_group_id)

    def __repr__(self):
        repr_ = '{}(sqs_queue={}, receiver={})'
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._receiver)
