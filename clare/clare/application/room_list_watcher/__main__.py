# -*- coding: utf-8 -*-

from clare import infrastructure
from clare.application import room_list_watcher
from clare.main import get_configuration

if __name__ == '__main__':
    properties = get_configuration()

    infrastructure_factory = infrastructure.factories.ApplicationInfrastructure(
        properties=properties)
    infrastructure = infrastructure_factory.create()

    producer_factory = room_list_watcher.factories.RoomListWatcher(
        infrastructure=infrastructure.room_list_watcher,
        properties=properties['room_list_watcher'])
    producer = producer_factory.create()

    producer.produce(interval=properties['room_list_watcher']['interval'])
