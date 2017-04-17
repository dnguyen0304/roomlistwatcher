# -*- coding: utf-8 -*-

import itertools

import pandas as pd

from .. import models


class BattleMetricsService(object):

    _mapping = {
        models.PlayerRecord: '_handle_player_record',
        models.PokemonRecord: '_handle_pokemon_record',
        models.SwitchRecord: '_handle_switch_record'
    }

    def __init__(self):
        self._battle = models.Battle()

    def read_html(self, file_path):
        battle_log = models.BattleLog.from_html(file_path=file_path)
        self._load_battle(battle_log=battle_log)

    def _load_battle(self, battle_log):
        for record in battle_log.records:
            try:
                handler = getattr(self, self._mapping[type(record)])
            except KeyError:
                pass
            else:
                handler(record)

    def _handle_player_record(self, record):
        player = models.Player(name=record.name)
        self._battle.add_player(position=record.position, player=player)

    def _handle_pokemon_record(self, record):
        pokemon = models.Pokemon(name=record.pokemon_name)
        player = self._battle.get_player(position=record.position)
        player.pokemon.append(pokemon)

    def _handle_switch_record(self, record):
        player = self._battle.get_player(position=record.position)
        for pokemon in player.pokemon:
            if pokemon.name == record.pokemon_name:
                pokemon.total_hit_points = record.total_hit_points
                break

    @property
    def summary(self):
        data = list()
        for player in self._battle.get_all_players():
            pokemon_names = (pokemon.name for pokemon in player.pokemon)
            data.extend(itertools.product([player.name], pokemon_names))
        columns = ['player_name', 'pokemon_name']
        return pd.DataFrame.from_records(data=data, columns=columns)
