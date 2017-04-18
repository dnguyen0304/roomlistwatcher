# -*- coding: utf-8 -*-

import collections

import pandas as pd

from .. import models


class BattleMetricsService(object):

    def __init__(self):
        self._pokemon_index = collections.defaultdict(dict)
        self._battle = models.Battle()
        self.summary = pd.DataFrame()

    def read_html(self, file_path):
        log = models.BattleLog.from_html(file_path=file_path)
        self._handle_log_records(log.records)

    def read_string(self, data):
        log = models.BattleLog.from_string(data=data)
        self._handle_log_records(log.records)

    def _handle_log_records(self, log_records):
        for log_record in log_records:
            self._battle.apply_log_record(log_record)
            # While there is a pd.Index.any method, pd.MultiIndex
            # objects do not support any type of truth testing. You
            # must instead rely on the isinstance or type functions.
            summary_has_index = isinstance(self.summary, pd.MultiIndex)
            if not summary_has_index and self._battle.pokemon_are_loaded:
                self.summary = self._create_index()

    def _create_index(self):
        tuples = list()
        for player in self._battle.get_all_players():
            for pokemon in player.pokemon:
                tuples.append((player.name, pokemon.name))
                self._pokemon_index[player.name][pokemon.name] = pokemon
        names = ['player_name', 'pokemon_name']
        index = pd.MultiIndex.from_tuples(tuples, names=names)
        summary = pd.DataFrame(index=index)
        return summary
