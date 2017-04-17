# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal, assert_in

from .. import BattleMetricsService
from morpha import models


class TestBattleMetricsService(object):

    def __init__(self):
        self.service = None

    def setup(self):
        self.service = BattleMetricsService()

    def test_load_battle(self):
        self.mock_record_handlers()

        battle_log = models.BattleLog._from_string(data='|player|p1|foo|0')
        self.service._load_battle(battle_log=battle_log)
        self.service._handle_player_record.assert_called()

    def test_load_battle_missing_handler(self):
        class MockBattleLog(object):
            records = list()

        self.mock_record_handlers()

        battle_log = MockBattleLog()
        battle_log.records.append('foo')
        self.service._load_battle(battle_log=battle_log)

    def test_handle_player_record(self):
        self.run_player_record_handler()

        player = self.service._battle.get_player(position=1)
        assert_equal(player.name, 'foo')

    def test_handle_pokemon_record(self):
        self.run_player_record_handler()
        self.run_pokemon_record_handler()

        player = self.service._battle.get_player(position=1)
        assert_equal(player.pokemon[0].name, 'bar')

    def test_handle_switch_record(self):
        self.run_player_record_handler()
        self.run_pokemon_record_handler()
        self.run_switch_record_handler()

        player = self.service._battle.get_player(position=1)
        assert_equal(player.pokemon[0].total_hit_points, 100)

    def test_summary_fields(self):
        self.run_player_record_handler()
        self.run_pokemon_record_handler()

        assert_in('player_name', self.service.summary.columns)
        assert_in('pokemon_name', self.service.summary.columns)

    def mock_record_handlers(self):
        self.service._handle_player_record = mock.MagicMock()
        self.service._handle_pokemon_record = mock.MagicMock()

    def run_player_record_handler(self):
        record = models.PlayerRecord(position=1, name='foo')
        self.service._handle_player_record(record)

    def run_pokemon_record_handler(self):
        record = models.PokemonRecord(position=1, pokemon_name='bar')
        self.service._handle_pokemon_record(record)

    def run_switch_record_handler(self):
        record = models.SwitchRecord(position=1,
                                     pokemon_name='bar',
                                     remaining_hit_points=0,
                                     total_hit_points=100)
        self.service._handle_switch_record(record)
