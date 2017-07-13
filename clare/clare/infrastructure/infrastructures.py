# -*- coding: utf-8 -*-


class DownloadBot(object):

    def __init__(self, consume_from_queue):

        """
        Parameters
        ----------
        consume_from_queue : typing.Type[clare.infrastructure.interfaces.IQueue]
        """

        self.consume_from_queue = consume_from_queue

    def __repr__(self):
        repr_ = '{}(consume_from_queue={})'
        return repr_.format(self.__class__.__name__, self.consume_from_queue)


class RoomListWatcher(object):

    def __init__(self, produce_to_queue):

        """
        Parameters
        ----------
        produce_to_queue : typing.Type[clare.infrastructure.interfaces.IQueue]
        """

        self.produce_to_queue = produce_to_queue

    def __repr__(self):
        repr_ = '{}(produce_to_queue={})'
        return repr_.format(self.__class__.__name__, self.produce_to_queue)


class Application(object):

    def __init__(self,
                 room_list_watcher_infrastructure,
                 download_bot_infrastructure):

        """
        Parameters
        ----------
        room_list_watcher_infrastructure : clare.infrastructure.infrastructures.RoomListWatcher
        download_bot_infrastructure : clare.infrastructure.infrastructures.DownloadBot
        """

        self.room_list_watcher = room_list_watcher_infrastructure
        self.download_bot = download_bot_infrastructure

    def __repr__(self):
        repr_ = ('{}('
                 'room_list_watcher_infrastructure={}, '
                 'download_bot_infrastructure={})')
        return repr_.format(self.__class__.__name__,
                            self.room_list_watcher,
                            self.download_bot)
