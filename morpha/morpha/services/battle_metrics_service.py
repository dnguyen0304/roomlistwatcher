# -*- coding: utf-8 -*-

import pandas as pd

from ..models import BattleLog


class BattleMetricsService(object):

    def __init__(self):
        self.summary = None

    def read_html(self, file_path):
        battle_log = BattleLog.from_html(file_path=file_path)
        self._help_read_html(battle_log=battle_log)

    def _help_read_html(self, battle_log):
        data = (record.__dict__ for record in battle_log.records)
        self.summary = pd.DataFrame(data=data)
