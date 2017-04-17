# -*- coding: utf-8 -*-

import itertools

import pandas as pd

from .. import models


class BattleMetricsService(object):

    def __init__(self):
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
            if self._battle.pokemon_are_loaded:
                index = self._construct_index()
                self.summary = pd.DataFrame(index=index)

    def _construct_index(self):
        tuples = list()
        for player in self._battle.get_all_players():
            pokemon_names = (pokemon.name for pokemon in player.pokemon)
            tuples.extend(itertools.product([player.name], pokemon_names))
        names = ['player_name', 'pokemon_name']
        index = pd.MultiIndex.from_tuples(tuples, names=names)
        return index
