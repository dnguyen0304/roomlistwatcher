# -*- coding: utf-8 -*-

import datetime
import time


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


def should_stop(maximum_duration, start_time, _get_now_in_seconds=None):

    """
    Parameters
    ----------
    maximum_duration : float
        Maximum duration in seconds since the epoch.
    start_time : float
        Start time in seconds since the epoch.
    _get_now_in_seconds : collections.Callable
        Used internally. Defaults to time.time.

    Returns
    -------
    bool
        True if the process should stop.
    """

    get_now_in_seconds = _get_now_in_seconds or time.time

    now = get_now_in_seconds()
    current_duration = now - start_time
    if current_duration >= maximum_duration:
        result = True
    else:
        result = False

    return result
