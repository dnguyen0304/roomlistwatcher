# -*- coding: utf-8 -*-

from . import TeamPreviewRecord


class Parser(object):

    parsers = {'poke': TeamPreviewRecord}

    def parse(self, data):
        records = list()
        for record_id, message in enumerate(data.split('\n')):
            topic = message.split('|')[1]
            try:
                record = self.parsers[topic].from_message(message)
            except KeyError:
                pass
            else:
                record.record_id = record_id + 1
                records.append(record)
        return records


class BattleLog(object):

    def __init__(self):
        self.battle_log_id = 0
        self.records = list()

    @classmethod
    def _from_string(cls, data):
        battle_log = cls()
        battle_log.records = Parser().parse(data=data)
        return battle_log

    def __repr__(self):
        repr_ = '{}(battle_log_id={})'
        return repr_.format(self.__class__.__name__, self.battle_log_id)
