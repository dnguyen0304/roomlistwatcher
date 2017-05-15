# -*- coding: utf-8 -*-

import json

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
    data = json.loads(message)

    assert_equal(data['exception_type'], 'clare.scraping.tests.test_scraper.Mock')
    assert_equal(data['exception_message'], 'foo')
