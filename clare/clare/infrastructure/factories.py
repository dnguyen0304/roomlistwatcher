# -*- coding: utf-8 -*-

import Queue as queue
import httplib

import boto3
import botocore.errorfactory

from . import adapters
from . import infrastructures


class Queue(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.application.infrastructure.interfaces.IQueue]
        """

        queue_ = queue.Queue()
        queue_ = adapters.QueueToQueue(queue=queue_,
                                       properties=self._properties)
        return queue_

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class SqsFifoQueue(object):

    _SERVICE_NAME = 'sqs'

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.application.infrastructure.interfaces.IQueue]
        """

        # Find the existing queue resource or create a new one.
        session = boto3.session.Session(
            profile_name=self._properties['administrator.profile.name'])
        client = session.client(service_name=SqsFifoQueue._SERVICE_NAME)

        try:
            response = client.get_queue_url(QueueName=self._properties['name'])
        except botocore.errorfactory.QueueDoesNotExist:
            response = client.create_queue(
                QueueName=self._properties['name'],
                Attributes={
                    'FifoQueue': 'True',
                    'VisibilityTimeout': str(self._properties['message.visibility.timeout.seconds']),
                    'MessageRetentionPeriod': str(self._properties['message.retention.seconds']),
                    'MaximumMessageSize': str(self._properties['message.maximum.bytes']),
                    'DelaySeconds': str(self._properties['message.delay.seconds']),
                    'ContentBasedDeduplication': 'True'
                }
            )

        if response['ResponseMetadata']['HTTPStatusCode'] != httplib.OK:
            raise Exception(str(response))
        else:
            queue_url = response['QueueUrl']

        # Create the queue.
        session = boto3.session.Session(
            profile_name=self._properties['profile.name'])
        sqs_resource = session.resource(service_name=SqsFifoQueue._SERVICE_NAME)

        sqs_queue = sqs_resource.Queue(url=queue_url)
        queue_ = adapters.SqsFifoQueueToQueue(sqs_queue=sqs_queue,
                                              properties=self._properties)

        return queue_

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class ApplicationInfrastructure(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):

        """
        Returns
        -------
        clare.infrastructure.infrastructures.ApplicationInfrastructure
        """

        # Create the queue from the room list watcher to the
        # download bot.
        queue_factory = SqsFifoQueue(
            properties=self._properties['room_list_watcher']['queues']['produce_to'])
        produce_to_queue = queue_factory.create()

        # Create the room list watcher infrastructure.
        room_list_watcher_infrastructure = infrastructures.RoomListWatcher(
            produce_to_queue=produce_to_queue)

        # Create the queue from the room list watcher to the
        # download bot.
        queue_factory = SqsFifoQueue(
            properties=self._properties['download_bot']['queues']['consume_from'])
        consume_from_queue = queue_factory.create()

        # Create the download bot infrastructure.
        download_bot_infrastructure = infrastructures.DownloadBot(
            consume_from_queue=consume_from_queue)

        # Create the application infrastructure.
        application_infrastructure = infrastructures.Application(
            room_list_watcher_infrastructure=room_list_watcher_infrastructure,
            download_bot_infrastructure=download_bot_infrastructure)

        return application_infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
