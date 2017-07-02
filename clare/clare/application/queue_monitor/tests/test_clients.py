# -*- coding: utf-8 -*-

import Queue as Queue

from nose.tools import assert_equal

from .. import clients


def test_client_calculate_message_count():

    queue = Queue.Queue()
    queue_client = clients.Client(queue=queue)

    expected = len('foo')
    for i in xrange(expected):
        queue.put(i)

    assert_equal(queue_client.calculate_message_count(), expected)
