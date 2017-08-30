# -*- coding: utf-8 -*-

import json

from nose.tools import assert_equal

from .. import utility


class Mock(Exception):
    pass


def test_format_exception():

    try:
        raise Mock('foo')
    except Mock as e:
        pass

    message = utility.format_exception(e=e)
    data = json.loads(message)

    assert_equal(data['exception_type'], __name__ + '.' + Mock.__name__)
    assert_equal(data['exception_message'], 'foo')
