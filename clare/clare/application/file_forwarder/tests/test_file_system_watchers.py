# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_false

from .. import file_system_watchers
from .. import interfaces


class MockHandler(interfaces.IHandler):

    def handle(self, event):
        pass


def mock_stream(value):
    yield value


class TestFileSystemWatcher(object):

    def __init__(self):
        self.mock_handler = None

    def setup(self):
        self.mock_handler = MockHandler()
        self.mock_handler.handle = mock.Mock()

    def test_start(self):
        value = 'foo'
        stream = mock_stream(value=value)
        file_system_watcher = file_system_watchers.FileSystemWatcher(
            stream=stream,
            handler=self.mock_handler)
        file_system_watcher.start()
        self.mock_handler.handle.assert_called_with(event=value)

    def test_start_filters_null_events(self):
        value = None
        stream = mock_stream(value=value)
        file_system_watcher = file_system_watchers.FileSystemWatcher(
            stream=stream,
            handler=self.mock_handler)
        file_system_watcher.start()
        assert_false(self.mock_handler.handle.called)
