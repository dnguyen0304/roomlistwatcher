# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import assert_equal, raises

from .. import receivers
from clare.common.messaging import consumer
from clare.common.messaging import factories


class MockSqsQueue(object):

    def receive_messages(self):
        pass


class TestSqsReceiver(object):

    def __init__(self):
        self.message_factory = None
        self.messages = None
        self.message = None

    def setup(self):
        self.message_factory = factories.Message()

        self.messages = list()
        self.messages.append(factories.Message().create(body='foo'))
        self.messages.append(factories.Message().create(body='bar'))

        self.message = self.messages[0]

    def test_receive(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=[self.message])

        receiver = receivers.SqsReceiver(sqs_queue=sqs_queue,
                                         batch_size_count=None,
                                         wait_time_seconds=None,
                                         message_factory=self.message_factory)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    @raises(consumer.exceptions.ReceiveTimeout)
    def test_receive_raises_exception(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=list())

        receiver = receivers.SqsReceiver(sqs_queue=sqs_queue,
                                         batch_size_count=None,
                                         wait_time_seconds=None,
                                         message_factory=None)
        receiver.receive()

    def test_receive_from_buffer(self):
        _buffer = collections.deque()
        _buffer.append(self.message)

        receiver = receivers.SqsReceiver(sqs_queue=None,
                                         batch_size_count=None,
                                         wait_time_seconds=None,
                                         message_factory=None,
                                         _buffer=_buffer)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    def test_minimize_batch_size_count(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=self.messages)

        receiver = receivers.SqsReceiver(sqs_queue=sqs_queue,
                                         batch_size_count=None,
                                         wait_time_seconds=None,
                                         message_factory=self.message_factory)
        receiver.minimize_batch_size_count()
        receiver.receive()
        sqs_queue.receive_messages.assert_called_with(
            MaxNumberOfMessages=receivers.SqsReceiver.BATCH_SIZE_MINIMUM_COUNT,
            WaitTimeSeconds=None)

    def test_restore_batch_size_count(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=self.messages)

        batch_size_count = len(self.messages)

        receiver = receivers.SqsReceiver(sqs_queue=sqs_queue,
                                         batch_size_count=batch_size_count,
                                         wait_time_seconds=None,
                                         message_factory=self.message_factory)
        receiver.minimize_batch_size_count()
        receiver.restore_batch_size_count()
        receiver.receive()
        sqs_queue.receive_messages.assert_called_with(
            MaxNumberOfMessages=batch_size_count,
            WaitTimeSeconds=None)
