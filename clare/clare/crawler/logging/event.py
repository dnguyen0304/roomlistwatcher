# -*- coding: utf-8 -*-

import abc
import collections
import datetime
import json
import uuid


class IJsonSerializable(object):

    @abc.abstractmethod
    def to_json(self):

        """
        Returns
        -------
        str
        """

        pass


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


class Event(IJsonSerializable):

    INTERFACE_VERSION = '1.0.0'

    def __init__(self, topic, arguments):

        """
        Parameters
        ----------
        topic : Topic
        arguments : IJsonSerializable
        """

        self.correlation_id = str(uuid.uuid4())

        self.topic = topic
        self.arguments = arguments

        self.created_at = datetime.datetime.utcnow().replace(tzinfo=utc)

    def to_json(self):
        data = collections.OrderedDict((
            ('interface_version', self.INTERFACE_VERSION),
            ('correlation_id', self.correlation_id),
            ('topic', self.topic.name),
            ('arguments', self.arguments.to_json()),
            ('created_at', self.created_at.isoformat())))
        return json.dumps(data)

    def __repr__(self):
        repr_ = '{}(topic={}, arguments={})'
        return repr_.format(self.__class__.__name__,
                            self.topic,
                            self.arguments)


utc = UTC()
