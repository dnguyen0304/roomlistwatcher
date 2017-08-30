# -*- coding: utf-8 -*-

import collections
import json
import os

_ENVIRONMENT_VARIABLE_NAME = 'ROOM_LIST_WATCHER_CONFIGURATION_FILE_PATH'


def get_configuration():

    """
    Read the application configuration.
    """

    configuration_file_path = os.environ[_ENVIRONMENT_VARIABLE_NAME]

    with open(configuration_file_path, 'rb') as file:
        parsed_configuration = json.loads(file.read())

    return parsed_configuration


def format_exception(e):

    """
    Parameters
    ----------
    e : exceptions.Exception

    Returns
    -------
    str
    """

    data = collections.OrderedDict()
    data['exception_type'] = type(e).__module__ + '.' + e.__class__.__name__
    data['exception_message'] = e.message

    return json.dumps(data)
