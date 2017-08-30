# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is_not_none, assert_true

from .. import filters
from .. import flush_strategies


class TestNoDuplicateString(object):

    def __init__(self):
        self.string = self.duplicate = None

    def setup(self):
        self.string = self.duplicate = 'foo'

    def test_flush_strategy(self):
        flush_strategy = flush_strategies.AfterSize(maximum_size=1)
        filter_ = filters.NoDuplicateString(flush_strategy=flush_strategy)
        filter_.filter(string=self.string)
        string = filter_.filter(string=self.string)
        assert_is_not_none(string)

    def test_should_filter_unique_body_should_not_filter(self):
        filter_ = filters.NoDuplicateString(flush_strategy=None)
        filter_._should_filter(string=self.string)
        unique = 'bar'
        should_filter = filter_._should_filter(string=unique)
        assert_false(should_filter)

    def test_should_filter_duplicate_body_should_filter(self):
        filter_ = filters.NoDuplicateString(flush_strategy=None)
        filter_._should_filter(string=self.string)
        should_filter = filter_._should_filter(string=self.duplicate)
        assert_true(should_filter)
