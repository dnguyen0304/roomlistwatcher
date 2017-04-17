# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal

from .. import Battle, BattleLog, PlayerRecord, PokemonRecord, SwitchRecord


class TestBattle(object):

    def __init__(self):
        self.player_record = None
        self.pokemon_record = None
        self.switch_record = None
        self.battle = Battle()

    def setup(self):
        self.player_record = PlayerRecord(position=1, name='foo')
        self.pokemon_record = PokemonRecord(
            position=self.player_record.position,
            pokemon_name='bar')
        self.switch_record = SwitchRecord(
            position=self.player_record.position,
            pokemon_name=self.pokemon_record.pokemon_name,
            remaining_hit_points=0,
            total_hit_points=100)

    def test_import_log(self):
        self.mock_record_handlers()

        log = BattleLog.from_string(data='|player|p1|foo|0')
        self.battle.import_log(log)
        self.battle.handle_player_record.assert_called()

    def test_import_log_missing_handler(self):
        class MockBattleLog(object):
            records = list()

        self.mock_record_handlers()

        log = MockBattleLog()
        log.records.append('foo')
        self.battle.import_log(log)

    def test_handle_player_record(self):
        self.battle.handle_player_record(self.player_record)

        player = self.battle.get_all_players()[0]
        assert_equal(player.name, self.player_record.name)

    def test_handle_pokemon_record(self):
        self.battle.handle_player_record(self.player_record)
        self.battle.handle_pokemon_record(self.pokemon_record)

        player = self.battle.get_all_players()[0]
        assert_equal(player.pokemon[0].name, self.pokemon_record.pokemon_name)

    def test_handle_switch_record(self):
        self.battle.handle_player_record(self.player_record)
        self.battle.handle_pokemon_record(self.pokemon_record)
        self.battle.handle_switch_record(self.switch_record)

        player = self.battle.get_all_players()[0]
        assert_equal(player.pokemon[0].total_hit_points,
                     self.switch_record.total_hit_points)

    def mock_record_handlers(self):
        for attribute in dir(self.battle):
            if attribute.startswith('handle') and attribute.endswith('record'):
                setattr(self.battle, attribute, mock.MagicMock())
