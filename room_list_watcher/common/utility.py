# -*- coding: utf-8 -*-

import collections
import datetime
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


# This implementation closely mirrors the UTC class in pytz and
# subsequently also the one in the Python Standard Library
# documentation.
class UTC(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return datetime.timedelta(0)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)

    def __str__(self):
        return 'UTC'


class TimeZone(object):

    @classmethod
    def from_name(cls, name):

        """
        Parameters
        ----------
        name : str

        Returns
        -------
        datetime.tzinfo
        """

        return UTC()
