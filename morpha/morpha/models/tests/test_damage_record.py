# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import DamageRecord


class TestDamageRecord(object):

    def test_from_message(self):
        message = '|-damage|p1a: Foo-Bar Foobar|10\/100'
        record = DamageRecord.from_message(message)
        assert_equal(record.taken_by_position, 1)
        assert_equal(record.taken_by_pokemon_name, 'Foo-Bar Foobar')
        assert_equal(record.remaining_hit_points, 10)
        assert_equal(record.total_hit_points, 100)
        assert_equal(record.indirectly_dealt_by, '')

    def test_from_message_faint_status_condition(self):
        message = '|-damage|p1a: Foo-Bar Foobar|0 fnt'
        record = DamageRecord.from_message(message)
        assert_equal(record.taken_by_position, 1)
        assert_equal(record.taken_by_pokemon_name, 'Foo-Bar Foobar')
        assert_equal(record.remaining_hit_points, 0)
        assert_equal(record.total_hit_points, 0)
        assert_equal(record.indirectly_dealt_by, '')

    def test_from_message_indirect_damage(self):
        message = '|-damage|p1a: Foo-Bar Foobar|10\/100|[from] Stealth Rock'
        record = DamageRecord.from_message(message)
        assert_equal(record.taken_by_position, 1)
        assert_equal(record.taken_by_pokemon_name, 'Foo-Bar Foobar')
        assert_equal(record.remaining_hit_points, 10)
        assert_equal(record.total_hit_points, 100)
        assert_equal(record.indirectly_dealt_by, 'Stealth Rock')

    @raises(ValueError)
    def test_from_message_incorrect_format(self):
        message = '|foo'
        DamageRecord.from_message(message)
