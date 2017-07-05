# -*- coding: utf-8 -*-


class FileSystemWatcher(object):

    def __init__(self, stream, handler):

        """
        Parameters
        ----------
        stream : collections.Iterable
        handler : clare.application.file_forwarder.interfaces.IHandler
        """

        self._stream = stream
        self._handler = handler

    def start(self):
        for event in self._stream:
            if event is not None:
                self._handler.handle(event=event)

    def __repr__(self):
        repr_ = '{}(stream={}, handler={})'
        return repr_.format(self.__class__.__name__,
                            self._stream,
                            self._handler)
