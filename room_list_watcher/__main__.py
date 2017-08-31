# -*- coding: utf-8 -*-

from room_list_watcher import factories
from room_list_watcher import infrastructure
from room_list_watcher.common import utility

if __name__ == '__main__':
    properties = utility.get_configuration()

    infrastructure_factory = infrastructure.factories.RoomListWatcherInfrastructure(
        properties=properties)
    infrastructure = infrastructure_factory.create()

    application_factory = factories.RoomListWatcherApplication(
        infrastructure=infrastructure,
        properties=properties)
    application = application_factory.create()

    application.start()
