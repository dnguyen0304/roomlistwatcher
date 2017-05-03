# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is_none, assert_true

from .. import Room
from .common import MockDocument


class TestRoom(object):

    def test_from_document_is_empty(self):
        string = """
<body>
  <a class="roomtab button cur closable">
    <span>(empty room)</span>
  </a>
</body>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_true(room.is_empty)
        assert_is_none(room.has_replay)

    def test_from_document_is_not_empty(self):
        string = """
<body>
  <a class="roomtab button cur closable">
    <span></span>
  </a>
</body>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_false(room.is_empty)
        assert_is_none(room.has_replay)

    def test_from_document_has_replay(self):
        string = """<a class="replayDownloadButton"></a>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_is_none(room.is_empty)
        assert_true(room.has_replay)

    def test_from_document_does_not_have_replay(self):
        string = """<a class="foo"></a>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_is_none(room.is_empty)
        assert_false(room.has_replay)
