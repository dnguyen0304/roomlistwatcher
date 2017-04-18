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
            # While there is a pd.Index.any method, pd.MultiIndex
            # objects do not support truth testing. You must instead
            # rely on the isinstance or type functions.
            summary_has_index = isinstance(self.summary.index, pd.MultiIndex)
            if not summary_has_index and self._battle.pokemon_are_loaded:
                self.summary = self._create_index()
                self.summary = self._create_metrics()
            if isinstance(log_record, models.DamageRecord):
                self.summary = self._update_damage_dealt(log_record=log_record)

    def _create_index(self):
        tuples = list()
        for player in self._battle.get_all_players():
            pokemon_names = (pokemon.name for pokemon in player.pokemon)
            tuples.extend(itertools.product([player.name], pokemon_names))

        names = ['player_name', 'pokemon_name']
        index = pd.MultiIndex.from_tuples(tuples, names=names)
        summary = pd.DataFrame(index=index)

        return summary

    def _create_metrics(self):
        summary = self.summary.copy()
        summary.loc[:, 'damage_dealt'] = 0
        return summary

    def _update_damage_dealt(self, log_record):
        summary = self.summary.copy()

        current_action = self._battle.current_action
        hit_points_before = current_action.targeted_pokemon.remaining_hit_points
        hit_points_after = log_record.remaining_hit_points
        hit_points_delta = hit_points_before - hit_points_after

        index = (current_action.used_by_player.name,
                 current_action.used_by_pokemon.name)
        summary.loc[index, 'damage_dealt'] += hit_points_delta

        return summary
