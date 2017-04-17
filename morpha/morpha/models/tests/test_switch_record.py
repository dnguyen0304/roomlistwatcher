# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import SwitchRecord


class TestSwitchRecord(object):

    def test_from_message(self):
        message = '|switch|p1a: Foo|Bar|10\/100'
        record = SwitchRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'Bar')
        assert_equal(record.remaining_hit_points, 10)
        assert_equal(record.total_hit_points, 100)

    def test_from_message_with_details(self):
        message = '|switch|p1a: Foo|Bar, F|10\/100'
        record = SwitchRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'Bar')
        assert_equal(record.remaining_hit_points, 10)
        assert_equal(record.total_hit_points, 100)

    @raises(ValueError)
    def test_from_message_unmatched_pattern(self):
        message = '|foo'
        SwitchRecord.from_message(message)
