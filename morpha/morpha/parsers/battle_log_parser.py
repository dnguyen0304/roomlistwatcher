# -*- coding: utf-8 -*-

from . import TeamPreviewRecordParser


class BattleLogParser(object):

    parsers = {'poke': TeamPreviewRecordParser}

    def parse(self, data):
        records = list()
        for record_id, message in enumerate(data.split('\n')):
            topic = message.split('|')[1]
            try:
                record = self.parsers[topic].parse(message=message)
            except KeyError:
                pass
            else:
                record.record_id = record_id + 1
                records.append(record)
        return records
