# -*- coding: utf-8 -*-

import itertools

import pandas as pd

from .. import models


class BattleMetricsService(object):

    def __init__(self):
        self._battle = models.Battle()

    def read_html(self, file_path):
        log = models.BattleLog.from_html(file_path=file_path)
        for log_record in log.records:
            self._battle.apply_log_record(log_record)

    def read_string(self, data):
        log = models.BattleLog.from_string(data=data)
        for log_record in log.records:
            self._battle.apply_log_record(log_record)

    @property
    def summary(self):
        data = list()
        for player in self._battle.get_all_players():
            pokemon_names = (pokemon.name for pokemon in player.pokemon)
            data.extend(itertools.product([player.name], pokemon_names))
        columns = ['player_name', 'pokemon_name']
        return pd.DataFrame.from_records(data=data, columns=columns)
