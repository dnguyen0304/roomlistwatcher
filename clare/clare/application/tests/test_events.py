# -*- coding: utf-8 -*-

import json

from nose.tools import assert_in, assert_less

from .. import events


class TestRoomCreated(object):

    def __init__(self):
        self.room_path = None
        self.event = None

    def setup(self):
        self.room_path = '/battle-foo-0'
        self.event = events.RoomCreated(room_path=self.room_path)

    def test_to_json_has_topic_name_key(self):
        data = json.loads(self.event.to_json())
        assert_in('topic_name', data)

    def test_to_json_has_arguments_key(self):
        data = json.loads(self.event.to_json())
        assert_in('arguments', data)

    def test_to_json_is_ordered(self):
        serialized = self.event.to_json()
        topic_name_key_start = serialized.index('topic_name')
        arguments_key_start = serialized.index('arguments')
        assert_less(topic_name_key_start, arguments_key_start)
