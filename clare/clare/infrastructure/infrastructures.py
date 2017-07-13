# -*- coding: utf-8 -*-


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
