# -*- coding: utf-8 -*-

import Queue as queue
import httplib

import boto3

from . import adapters
from . import infrastructures

ADMINISTRATOR_ROLE_NAME = 'administrator'
PRODUCER_ROLE_NAME = 'producer'


class Queue(object):

    _adapter_type = adapters.QueueToQueue

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.application.infrastructure.interfaces.IQueue]
        """

        queue_ = queue.Queue()
        queue_ = self._adapter_type(queue=queue_)
        return queue_

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


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

        # Create the queue resource.
        session = self._create_session(role_name=ADMINISTRATOR_ROLE_NAME)
        client = session.client(service_name=SqsFifoQueue._SERVICE_NAME)

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
        session = self._create_session(role_name=PRODUCER_ROLE_NAME)
        sqs_resource = session.resource(service_name=SqsFifoQueue._SERVICE_NAME)

        sqs_queue = sqs_resource.Queue(url=queue_url)
        queue_ = adapters.SqsFifoQueueToQueue(sqs_queue=sqs_queue)

        return queue_

    @staticmethod
    def _create_session(role_name):

        """
        Parameters
        ----------
        role_name : str

        Returns
        -------
        Boto3 Session
        """

        profile_name = SQS_SERVICE_NAME + '.' + role_name
        session = boto3.session.Session(profile_name=profile_name)
        return session

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
        queue_ = queue_factory.create()

        # Create the room list watcher infrastructure.
        room_list_watcher_infrastructure = infrastructures.RoomListWatcher(
            produce_to_queue=queue_)

        # Create the download bot infrastructure.
        download_bot_infrastructure = infrastructures.DownloadBot(
            consume_from_queue=queue_)

        # Create the application infrastructure.
        application_infrastructure = infrastructures.Application(
            room_list_watcher_infrastructure=room_list_watcher_infrastructure,
            download_bot_infrastructure=download_bot_infrastructure)

        return application_infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
