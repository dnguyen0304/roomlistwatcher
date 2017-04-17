# -*- coding: utf-8 -*-

from nose.tools import assert_in

from .. import BattleMetricsService


class TestBattleMetricsService(object):

    def test_summary_fields(self):
        data = '\n'.join(['|player|p1|foo|0',
                          '|player|p2|bar|0',
                          '|poke|p1|eggs|item',
                          '|switch|p1a: egg|eggs|100\/100'])
        service = BattleMetricsService()
        service.read_string(data=data)
        assert_in('player_name', service.summary.index.names)
        assert_in('pokemon_name', service.summary.index.names)
