# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is_not_none, assert_true

from .. import filters
from .. import flush_strategies
from clare.common import messaging


class TestNoDuplicate(object):

    def __init__(self):
        self.first_record = self.duplicate_record = None

    def setup(self):
        self.first_record = self.duplicate_record = messaging.records.Record(
            queue_name=None,
            timestamp=None,
            value='foo')

    def test_flush_strategy(self):
        flush_strategy = flush_strategies.AfterSize(maximum_size=1)
        filter_ = filters.NoDuplicate(flush_strategy=flush_strategy)
        filter_.filter(record=self.first_record)
        record = filter_.filter(record=self.first_record)
        assert_is_not_none(record)

    def test_should_filter_unique_value_should_not_filter(self):
        filter_ = filters.NoDuplicate(flush_strategy=None)
        filter_._should_filter(record=self.first_record)
        new_record = messaging.records.Record(queue_name=None,
                                              timestamp=None,
                                              value='bar')
        should_filter = filter_._should_filter(record=new_record)
        assert_false(should_filter)

    def test_should_filter_duplicate_value_should_filter(self):
        filter_ = filters.NoDuplicate(flush_strategy=None)
        filter_._should_filter(record=self.first_record)
        should_filter = filter_._should_filter(record=self.duplicate_record)
        assert_true(should_filter)
