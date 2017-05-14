# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import scraper


class Mock(Exception):
    pass


def test_format_exception():

    try:
        raise Mock('foo')
    except Mock as e:
        pass

    message = scraper.format_exception(e=e)
    assert_equal(message, 'clare.scraping.tests.test_scraper.Mock: foo')
