# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_false, assert_true

from .. import main


class TestHtmlParser(object):

    def __init__(self):
        self.html_parser = None
        self.data = ''

    def setup(self):
        self.html_parser = main.HtmlParser()
        self.data = '<script class="battle-log-data">foo</script>'

    def test_interface(self):
        assert_true(hasattr(self.html_parser, 'processed_data'))

    def test_parse_battle_log_data(self):
        self.html_parser.feed(data=self.data)
        assert_equal(self.html_parser.processed_data, 'foo')

    def test_parse_battle_log_flag(self):
        self.html_parser.feed(data=self.data)
        assert_false(self.html_parser._is_battle_log)
