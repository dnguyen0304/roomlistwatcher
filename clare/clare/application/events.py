# -*- coding: utf-8 -*-

import collections
import json

from . import topics


class RoomCreated(object):

    topic = topics.RoomListWatcher.ROOM_CREATED

    def __init__(self, room_path):

        """
        Parameters
        ----------
        room_path : str
        """

        self.arguments = collections.OrderedDict()
        self.arguments['room_path'] = room_path

    def to_json(self):

        """
        Returns
        -------
        str
        """

        data = collections.OrderedDict()
        data['topic_name'] = self.topic.name
        data['arguments'] = self.arguments
        serialized = json.dumps(data, default=repr)
        return serialized

    def __repr__(self):
        repr_ = '{}(room_path="{}")'
        return repr_.format(self.__class__.__name__,
                            self.arguments['room_path'])
