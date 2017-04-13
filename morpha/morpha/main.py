# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 0):
    import HTMLParser as html_parser


class HtmlParser(html_parser.HTMLParser):

    def __init__(self):
        html_parser.HTMLParser.__init__(self)
        self._is_battle_log = False
        self.processed_data = ''

    def handle_starttag(self, tag, attributes):
        if tag == 'script':
            for attribute in attributes:
                if attribute[0] != 'class':
                    continue
                if attribute[1] == 'battle-log-data':
                    self._is_battle_log = True

    def handle_data(self, data):
        if self._is_battle_log:
            self._is_battle_log = False
            self.processed_data = data
