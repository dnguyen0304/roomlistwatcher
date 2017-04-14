# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import TeamPreviewRecordParser


class TestTeamPreviewRecordParser(object):

    def test_parse(self):
        message = '|poke|p1|Foo, F|item'
        record = TeamPreviewRecordParser.parse(message=message)
        assert_equal(record.player_id, 1)
        assert_equal(record.pokemon_name, 'Foo')

    def test_parse_without_gender(self):
        message = '|poke|p1|Foo|item'
        record = TeamPreviewRecordParser.parse(message=message)
        assert_equal(record.player_id, 1)
        assert_equal(record.pokemon_name, 'Foo')

    @raises(ValueError)
    def test_parse_incorrect_format(self):
        message = '|foo'
        TeamPreviewRecordParser.parse(message=message)
