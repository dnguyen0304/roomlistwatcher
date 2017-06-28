# -*- coding: utf-8 -*-

from nose.tools import assert_is, assert_is_none

from .. import filters
from clare.common import messaging


class TestOnlyGenerationSevenMetagame(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.OnlyGenerationSevenMetagame()

    def test_does_not_filter_generation_seven_metagame_battle(self):
        value = '/battle-gen7foo-0'
        input = messaging.records.Record(queue_name=None,
                                         timestamp=None,
                                         value=value)
        output = self.filter.filter(record=input)
        assert_is(output, input)

    def test_does_filter_non_generation_seven_metagame_battle(self):
        value = '/battle-gen0foo-0'
        record = messaging.records.Record(queue_name=None,
                                          timestamp=None,
                                          value=value)
        record = self.filter.filter(record=record)
        assert_is_none(record)


class TestOnlyOverusedMetagame(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.OnlyOverusedMetagame()

    def test_does_not_filter_overused_metagame_battle(self):
        value = '/battle-fooou-0'
        input = messaging.records.Record(queue_name=None,
                                         timestamp=None,
                                         value=value)
        output = self.filter.filter(record=input)
        assert_is(output, input)

    def test_does_filter_non_overused_metagame_battle(self):
        value = '/battle-foobar-0'
        record = messaging.records.Record(queue_name=None,
                                          timestamp=None,
                                          value=value)
        record = self.filter.filter(record=record)
        assert_is_none(record)
