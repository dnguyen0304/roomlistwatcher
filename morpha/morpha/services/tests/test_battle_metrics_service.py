# -*- coding: utf-8 -*-

from nose.tools import assert_in

from .. import BattleMetricsService


class TestBattleMetricsService(object):

    def test_summary_fields(self):
        data = '|player|p1|foo|0\n|poke|p1|bar|item'
        service = BattleMetricsService()
        service.read_string(data=data)
        assert_in('player_name', service.summary.columns)
        assert_in('pokemon_name', service.summary.columns)
