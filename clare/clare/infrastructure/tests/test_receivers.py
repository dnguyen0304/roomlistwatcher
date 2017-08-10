# -*- coding: utf-8 -*-

import collections
import itertools

import mock
from nose.tools import assert_equal, assert_raises, assert_true, raises

from .. import receivers
from clare.common.messaging import consumer
from clare.common.messaging import factories


class MockSqsQueue(object):

    def receive_messages(self):
        pass


class TestReceiver(object):

    def __init__(self):
        self.message_factory = None
        self._deque = None
        self._buffer = None

        self.data = None
        self.messages = None
        self.message = None

    def setup(self):
        self.message_factory = factories.Message2()
        self._deque = collections.deque()
        self._buffer = collections.deque()

        self.data = ('foo', 'bar', 'foobar')
        self.messages = list()
        for body in self.data:
            message = self.message_factory.create()
            message.body = body
            self.messages.append(message)
        self.message = self.messages[0]


class TestConcurrentLinkedDeque(TestReceiver):

    def test_receive_does_fill_when_buffer_is_empty(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))

        self._deque.extend(self.data)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _deque=self._deque,
            _buffer=self._buffer)

        expected_deque_count = len(self._deque) - batch_size_maximum_count

        message = receiver.receive()

        assert_equal(expected_deque_count, len(self._deque))
        assert_equal(batch_size_maximum_count - 1, len(self._buffer))
        assert_equal(self.message.body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_receive_does_not_fill_while_buffer_has_messages(self):
        self._deque.extend(self.data)
        self._buffer.append(self.message)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=None,
            countdown_timer=None,
            message_factory=None,
            _deque=self._deque,
            _buffer=self._buffer)

        expected_buffer_count = len(self._buffer) - 1

        message = receiver.receive()

        assert_equal(len(self.data), len(self._deque))
        assert_equal(expected_buffer_count, len(self._buffer))
        assert_equal(self.message.body, message.body)

    def test_receive_timeout_raises_exception(self):
        batch_size_maximum_count = 1
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=(False,))

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=None)

        assert_raises(consumer.exceptions.ReceiveTimeout, receiver.receive)

        assert_true(countdown_timer.reset.called)

    def test_receive_is_ordered(self):
        batch_size_maximum_count = len(self.data)
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))

        self._deque.extend(self.data)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _deque=self._deque)

        for expected_body in self.data:
            message = receiver.receive()
            assert_equal(expected_body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_receive_less_than_batch_size_minimum_returns_to_deque(self):
        batch_size_maximum_count = batch_size_minimum_count = 2
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=(False,))

        self._deque.append(self.message.body)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            batch_size_minimum_count=batch_size_minimum_count,
            countdown_timer=countdown_timer,
            message_factory=None,
            _deque=self._deque,
            _buffer=self._buffer)

        expected_deque_count = len(self._deque)

        assert_raises(consumer.exceptions.ReceiveTimeout, receiver.receive)
        assert_equal(expected_deque_count, len(self._deque))
        assert_equal(0, len(self._buffer))

        assert_true(countdown_timer.reset.called)

    def test_receive_less_than_batch_size_minimum_returns_to_deque_ordered(self):
        batch_size_maximum_count = batch_size_minimum_count = 3
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.chain((True, False), itertools.repeat(True)))

        self._deque.extend(self.data)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            batch_size_minimum_count=batch_size_minimum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _deque=self._deque)

        try:
            receiver.receive()
        except consumer.exceptions.ReceiveTimeout:
            receiver.minimize_batch_size_count()
        except Exception:
            raise

        for expected_body in self.data:
            message = receiver.receive()
            assert_equal(expected_body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_minimize_batch_size_count(self):
        batch_size_maximum_count = 2
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=(False,))

        self._deque.append(self.message.body)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _deque=self._deque,
            _buffer=self._buffer)

        expected_deque_count = len(self._deque) - receivers.BATCH_SIZE_MINIMUM_COUNT

        receiver.minimize_batch_size_count()
        message = receiver.receive()

        assert_equal(expected_deque_count, len(self._deque))
        assert_equal(receivers.BATCH_SIZE_MINIMUM_COUNT - 1, len(self._buffer))
        assert_equal(self.message.body, message.body)

        assert_true(countdown_timer.reset.called)

    def test_restore_batch_size_count(self):
        batch_size_maximum_count = 2
        countdown_timer = TestConcurrentLinkedDeque.create_mock_countdown_timer(
            has_time_remaining=itertools.repeat(True))

        self._deque.extend(self.data)

        receiver = receivers.ConcurrentLinkedDeque(
            batch_size_maximum_count=batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=self.message_factory,
            _deque=self._deque,
            _buffer=self._buffer)

        expected_deque_count = len(self._deque) - batch_size_maximum_count

        receiver.minimize_batch_size_count()
        receiver.restore_batch_size_count()
        message = receiver.receive()

        assert_equal(expected_deque_count, len(self._deque))
        assert_equal(batch_size_maximum_count - 1, len(self._buffer))
        assert_equal(self.message.body, message.body)

        assert_true(countdown_timer.reset.called)

    @staticmethod
    def create_mock_countdown_timer(has_time_remaining):

        """
        Parameters
        ----------
        has_time_remaining : collections.Iterable

        Returns
        -------
        mock.Mock
        """

        mock_countdown_timer = mock.Mock()
        type(mock_countdown_timer).has_time_remaining = mock.PropertyMock(
            side_effect=has_time_remaining)
        mock_countdown_timer.reset = mock.Mock()
        return mock_countdown_timer


class TestSqsFifo(TestReceiver):

    def test_receive_does_fill_when_buffer_is_empty(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=[self.message])

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=self.message_factory)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    def test_receive_does_not_fill_while_buffer_has_messages(self):
        self._buffer.append(self.message)

        receiver = receivers.SqsFifoQueue(sqs_queue=None,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=None,
                                          _buffer=self._buffer)
        message = receiver.receive()
        assert_equal(self.message.body, message.body)

    @raises(consumer.exceptions.ReceiveTimeout)
    def test_receive_timeout_raises_exception(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=list())

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=None)
        receiver.receive()

    def test_minimize_batch_size_count(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=self.messages)

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=None,
                                          wait_time_seconds=None,
                                          message_factory=self.message_factory)
        receiver.minimize_batch_size_count()
        receiver.receive()
        sqs_queue.receive_messages.assert_called_with(
            MaxNumberOfMessages=receivers.BATCH_SIZE_MINIMUM_COUNT,
            WaitTimeSeconds=None)

    def test_restore_batch_size_count(self):
        sqs_queue = MockSqsQueue()
        sqs_queue.receive_messages = mock.Mock(return_value=self.messages)

        batch_size_count = len(self.data)

        receiver = receivers.SqsFifoQueue(sqs_queue=sqs_queue,
                                          batch_size_maximum_count=batch_size_count,
                                          wait_time_seconds=None,
                                          message_factory=self.message_factory)
        receiver.minimize_batch_size_count()
        receiver.restore_batch_size_count()
        receiver.receive()
        sqs_queue.receive_messages.assert_called_with(
            MaxNumberOfMessages=batch_size_count,
            WaitTimeSeconds=None)
