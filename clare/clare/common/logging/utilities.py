# -*- coding: utf-8 -*-

import collections
import json


def format_exception(e):

    """
    Parameters
    ----------
    e : exceptions.BaseException

    Returns
    -------
    str
    """

    data = collections.OrderedDict()
    data['exception_type'] = type(e).__module__ + '.' + e.__class__.__name__
    data['exception_message'] = e.message

    return json.dumps(data)
