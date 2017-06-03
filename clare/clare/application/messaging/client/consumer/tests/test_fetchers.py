# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

from nose.tools import assert_equal

from .. import fetchers


def test_fetcher_pop():

    queue_ = queue.Queue()
    fetcher = fetchers.Fetcher(queue=queue_)
    data = {
        'queue_name': 'foo',
        'timestamp': 'bar',
        'value': 'foobar'
    }
    queue_.put(item=data)
    record = fetcher.pop(timeout=None)

    assert_equal(record.queue_name, data['queue_name'])
    assert_equal(record.timestamp, data['timestamp'])
    assert_equal(record.value, data['value'])
