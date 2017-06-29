# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

from nose.tools import assert_equal

from .. import queue_clients


def test_queue_client_calculate_message_count():

    queue_ = queue.Queue()
    queue_client = queue_clients.QueueClient(queue=queue_)

    expected = len('foo')
    for i in xrange(expected):
        queue_.put(i)

    assert_equal(queue_client.calculate_message_count(), expected)
