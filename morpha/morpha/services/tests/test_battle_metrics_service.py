# -*- coding: utf-8 -*-

from nose.tools import assert_in

from .. import BattleMetricsService


class TestBattleMetricsService(object):

    def __init__(self):
        self.service = None

    def setup(self):
        data = '\n'.join(['|player|p1|foo|0',
                          '|player|p2|bar|0',
                          '|poke|p1|eggs|item',
                          '|switch|p1a: egg|eggs|100\/100'])
        self.service = BattleMetricsService()
        self.service.read_string(data=data)

    def test_index(self):
        assert_in('player_name', self.service.summary.index.names)
        assert_in('pokemon_name', self.service.summary.index.names)
