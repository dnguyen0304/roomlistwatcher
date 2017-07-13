# -*- coding: utf-8 -*-


class RoomListWatcher(object):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : typing.Type[clare.infrastructure.interfaces.IQueue]
        """

        self.queue = queue

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self.queue)


class Application(object):

    def __init__(self, room_list_watcher_infrastructure):

        """
        Parameters
        ----------
        room_list_watcher_infrastructure : clare.infrastructure.infrastructures.RoomListWatcher
        """

        self.room_list_watcher = room_list_watcher_infrastructure

    def __repr__(self):
        repr_ = '{}(room_list_watcher_infrastructure={})'
        return repr_.format(self.__class__.__name__, self.room_list_watcher)
