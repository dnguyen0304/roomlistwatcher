# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_list_equal, assert_true

from .. import IRecordParser, BattleLogParser


class MockRecord(object):
    pass


class MockRecordParser(IRecordParser):

    @staticmethod
    def parse(message):
        return MockRecord()


class TestBattleLogParser(object):

    def __init__(self):
        self.parser = None

    def setup(self):
        self.parser = BattleLogParser()
        self.parser.parsers['mock'] = MockRecordParser

    def test_parse(self):
        data = '|mock|foo\n|mock|bar'
        records = self.parser.parse(data=data)
        assert_equal(len(records), 2)
        assert_true(all(isinstance(record, MockRecord) for record in records))

    def test_parse_unmapped_topics_fail_silently(self):
        data = '|foo\n|bar'
        records = self.parser.parse(data=data)
        assert_list_equal(records, list())

    def test_parse_updates_record_id(self):
        data = '|mock|foo\n|mock|bar'
        records = self.parser.parse(data=data)
        assert_true(all(hasattr(record, 'record_id') for record in records))
        assert_equal(records[0].record_id, 1)
        assert_equal(records[1].record_id, 2)
