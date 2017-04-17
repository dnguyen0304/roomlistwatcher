# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import PokemonRecord


class TestTeamPreviewRecord(object):

    def test_from_message(self):
        message = '|poke|p1|Foo, F|item'
        record = PokemonRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'Foo')

    def test_from_message_without_gender(self):
        message = '|poke|p1|Foo|item'
        record = PokemonRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'Foo')

    @raises(ValueError)
    def test_from_message_incorrect_format(self):
        message = '|foo'
        PokemonRecord.from_message(message)
