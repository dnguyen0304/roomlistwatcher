# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import MoveRecord


class TestMoveRecord(object):

    def test_from_message(self):
        message = '|move|p1a: foo|foobar|p2a: bar'
        record = MoveRecord.from_message(message)
        assert_equal(record.used_by_position, 1)
        assert_equal(record.used_by_pokemon_name, 'foo')
        assert_equal(record.move_name, 'foobar')
        assert_equal(record.targeted_position, 2)
        assert_equal(record.targeted_pokemon_name, 'bar')

    @raises(ValueError)
    def test_from_message_unmatched_pattern(self):
        message = '|foo'
        MoveRecord.from_message(message)
