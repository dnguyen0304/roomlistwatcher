# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal

from .. import scrapers


class TestBufferingSourceAdapter(object):

    def __init__(self):
        self.elements = None
        self.scraper = None
        self.source = None
        self.n = None

    def setup(self):
        self.elements = xrange(2)
        self.scraper = scrapers.Nop()
        self.scraper.scrape = mock.Mock(return_value=self.elements)
        self.source = scrapers.BufferingSourceAdapter(scraper=self.scraper,
                                                      url=None)
        self.n = len(self.elements)

    def test_scrape_is_not_called_while_buffer_has_elements(self):
        for i in xrange(self.n):
            self.source.emit()
        assert_equal(self.scraper.scrape.call_count, 1)

    def test_scrape_is_called_when_buffer_is_empty(self):
        for i in xrange(self.n + 1):
            self.source.emit()
        assert_equal(self.scraper.scrape.call_count, 2)

    def test_records_are_ordered_and_reversed(self):
        records = [self.source.emit() for i in xrange(self.n)]
        assert_equal(*map(list, (reversed(records), self.elements)))
