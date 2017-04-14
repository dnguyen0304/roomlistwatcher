# -*- coding: utf-8 -*-

from nose.tools import assert_in

from .. import BattleMetricsService
from morpha import models


class TestBattleMetricsService(object):

    def __init__(self):
        self.service = None

    def setup(self):
        self.service = BattleMetricsService()

    def test_summary_fields(self):
        data = '|poke|p1|Foo, F|item'
        battle_log = models.BattleLog._from_string(data=data)

        self.service._help_read_html(battle_log=battle_log)

        assert_in('player_id', self.service.summary.columns)
        assert_in('pokemon_name', self.service.summary.columns)
