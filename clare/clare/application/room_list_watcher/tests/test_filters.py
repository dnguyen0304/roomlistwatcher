# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is_not_none, assert_true

from .. import filters
from .. import flush_strategies
from clare.common import messaging


class TestNoDuplicateBody(object):

    def __init__(self):
        self.message_factory = None
        self.first_message = self.duplicate_message = None

    def setup(self):
        self.message_factory = messaging.factories.Message()
        message = self.message_factory.create(body='foo')
        self.first_message = self.duplicate_message = message

    def test_flush_strategy(self):
        flush_strategy = flush_strategies.AfterSize(maximum_size=1)
        filter_ = filters.NoDuplicateBody(flush_strategy=flush_strategy)
        filter_.filter(message=self.first_message)
        message = filter_.filter(message=self.first_message)
        assert_is_not_none(message)

    def test_should_filter_unique_body_should_not_filter(self):
        filter_ = filters.NoDuplicateBody(flush_strategy=None)
        filter_._should_filter(message=self.first_message)
        new_message = self.message_factory.create(body='bar')
        should_filter = filter_._should_filter(message=new_message)
        assert_false(should_filter)

    def test_should_filter_duplicate_body_should_filter(self):
        filter_ = filters.NoDuplicateBody(flush_strategy=None)
        filter_._should_filter(message=self.first_message)
        should_filter = filter_._should_filter(message=self.duplicate_message)
        assert_true(should_filter)
