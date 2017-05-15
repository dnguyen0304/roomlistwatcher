# -*- coding: utf-8 -*-

import collections
import datetime
import json
import uuid

from . import interfaces


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


class Event(interfaces.IEvent, interfaces.IJsonSerializable):

    def __init__(self, topic, arguments):

        """
        Parameters
        ----------
        topic : Topic
        arguments : collections.Mapping
        """

        self.correlation_id = str(uuid.uuid4())

        self.topic = topic
        self.arguments = arguments

        self.created_at = datetime.datetime.utcnow().replace(tzinfo=utc)

    @property
    def INTERFACE_VERSION(self):
        return '1.0.0'

    def to_json(self):
        data = collections.OrderedDict()
        data['interface_version'] = self.INTERFACE_VERSION
        data['correlation_id'] = self.correlation_id
        data['topic_name'] = self.topic.name
        data['arguments'] = self.arguments
        data['created_at'] = self.created_at.isoformat()

        return json.dumps(data)

    def __repr__(self):
        repr_ = '{}(topic={}, arguments={})'
        return repr_.format(self.__class__.__name__,
                            self.topic,
                            self.arguments)


utc = UTC()
