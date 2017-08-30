# -*- coding: utf-8 -*-

import Queue as queue
import httplib

import boto3
import botocore.exceptions

from . import deleters
from . import infrastructures
from . import receivers
from . import senders
from clare.common import messaging
from clare.common import utilities


class _ConcurrentLinkedQueue(object):

    def create(self):

        """
        Returns
        -------
        Queue.Queue
        """

        return queue.Queue()


class _ConcurrentLinkedQueueSender(object):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.producer.senders.Sender]
        """

        return senders.ConcurrentLinkedQueue(queue=self._queue)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class _ConcurrentLinkedQueueReceiver(object):

    def __init__(self, queue, batch_size_maximum_count, wait_time_seconds):

        """
        Parameters
        ----------
        queue : Queue.Queue
        batch_size_maximum_count : int
        wait_time_seconds : int
        """

        self._queue = queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.receivers.Receiver]
        """

        # Create the countdown timer.
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._wait_time_seconds)

        # Create the message factory.
        message_factory = messaging.factories.Message2()

        return receivers.ConcurrentLinkedQueue(
            queue=self._queue,
            batch_size_maximum_count=self._batch_size_maximum_count,
            countdown_timer=countdown_timer,
            message_factory=message_factory)

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class _NopDeleter(object):

    def create(self):
        return deleters.Nop()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class _SqsFifoQueue(object):

    SERVICE_NAME = 'sqs'

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
        str
        """

        session = boto3.session.Session(
            profile_name=self._properties['administrator.profile.name'])
        client = session.client(service_name=_SqsFifoQueue.SERVICE_NAME)

        try:
            queue_url = self._find_queue_resource(client=client)
        except botocore.exceptions.ClientError as e:
            # See this documentation.
            # http://botocore.readthedocs.io/en/latest/client_upgrades.html#error-handling
            if e.response['ResponseMetadata']['HTTPStatusCode'] != httplib.BAD_REQUEST:
                raise
            if e.response['Error']['Code'] != 'AWS.SimpleQueueService.NonExistentQueue':
                raise
            queue_url = self._create_queue_resource(client=client)

        return queue_url

    def _find_queue_resource(self, client):

        """
        Parameters
        ----------
        client : typing.Type[botocore.client.BaseClient]

        Returns
        -------
        str
            URL to the existing queue resource.

        Raises
        ------
        Exception
            If there was an error while trying to find the queue
            resource.
        botocore.exceptions.ClientError
            If there was an error caused by the client while trying to
            find the queue resource.
        """

        try:
            response = client.get_queue_url(QueueName=self._properties['name'])
        except Exception:
            raise

        if response['ResponseMetadata']['HTTPStatusCode'] != httplib.OK:
            raise Exception(str(response['Error']))

        return response['QueueUrl']

    def _create_queue_resource(self, client):

        """
        Parameters
        ----------
        client : typing.Type[botocore.client.BaseClient]

        Returns
        -------
        str
            URL to the newly created queue resource.

        Raises
        ------
        Exception
            If there was an error while trying to create the queue
            resource.
        """

        try:
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
        except Exception:
            raise

        if response['ResponseMetadata']['HTTPStatusCode'] != httplib.OK:
            raise Exception(str(response['Error']))

        return response['QueueUrl']

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)


class _SqsFifoQueueSender(object):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.producer.senders.Sender]
        """

        return senders.SqsFifoQueue(sqs_queue=self._sqs_queue)

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)


class _SqsFifoQueueReceiver(object):

    def __init__(self,
                 sqs_queue,
                 batch_size_maximum_count,
                 wait_time_seconds,
                 message_factory):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        batch_size_maximum_count : int
        wait_time_seconds : int
        message_factory : clare.common.messaging.factories.Message
        """

        self._sqs_queue = sqs_queue
        self._batch_size_maximum_count = batch_size_maximum_count
        self._wait_time_seconds = wait_time_seconds
        self._message_factory = message_factory

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.receivers.Receiver]
        """

        return receivers.SqsFifoQueue(
            sqs_queue=self._sqs_queue,
            batch_size_maximum_count=self._batch_size_maximum_count,
            wait_time_seconds=self._wait_time_seconds,
            message_factory=self._message_factory)

    def __repr__(self):
        repr_ = ('{}('
                 'sqs_queue={}, '
                 'batch_size_maximum_count={}, '
                 'wait_time_seconds={}, '
                 'message_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sqs_queue,
                            self._batch_size_maximum_count,
                            self._wait_time_seconds,
                            self._message_factory)


class _SqsFifoQueueDeleter(object):

    def __init__(self, sqs_queue):

        """
        Parameters
        ----------
        sqs_queue : boto3.resources.factory.sqs.Queue
        """

        self._sqs_queue = sqs_queue

    def create(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.deleters.Deleter]
        """

        return deleters.SqsFifoQueue(sqs_queue=self._sqs_queue)

    def __repr__(self):
        repr_ = '{}(sqs_queue={})'
        return repr_.format(self.__class__.__name__, self._sqs_queue)


class _QueueAbstractFactory(object):

    def __init__(self, sender_factory, receiver_factory, deleter_factory):
        self._sender_factory = sender_factory
        self._receiver_factory = receiver_factory
        self._deleter_factory = deleter_factory

    @classmethod
    def new_concurrent_linked(cls, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping

        Returns
        -------
        clare.infrastructure.factories._QueueAbstractFactory
        """

        # Create the queue.
        queue_ = _ConcurrentLinkedQueue().create()

        # Create the sender factory.
        sender_factory = _ConcurrentLinkedQueueSender(queue=queue_)

        # Create the receiver factory.
        properties_ = properties['download_bot']['queues']['consume_from']
        receiver_factory = _ConcurrentLinkedQueueReceiver(
            queue=queue_,
            batch_size_maximum_count=properties_['message.receive.maximum.count'],
            wait_time_seconds=properties_['message.receive.wait.seconds'])

        # Create the deleter factory.
        deleter_factory = _NopDeleter()

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            sender_factory=sender_factory,
            receiver_factory=receiver_factory,
            deleter_factory=deleter_factory)

        return queue_abstract_factory

    @classmethod
    def new_sqs_fifo(cls, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping

        Returns
        -------
        clare.infrastructure.factories._QueueAbstractFactory
        """

        # Create the SQS FIFO queue resource.
        queue_factory = _SqsFifoQueue(
            properties=properties['room_list_watcher']['queues']['produce_to'])
        queue_url = queue_factory.create()

        # Create the SQS FIFO queue to produce to.
        properties_ = properties['room_list_watcher']['queues']['produce_to']
        session = boto3.session.Session(
            profile_name=properties_['profile.name'])
        sqs_resource = session.resource(
            service_name=_SqsFifoQueue.SERVICE_NAME)
        sqs_queue = sqs_resource.Queue(url=queue_url)

        # Create the sender factory.
        sender_factory = _SqsFifoQueueSender(sqs_queue=sqs_queue)

        # Create the SQS FIFO queue to consume from.
        properties_ = properties['download_bot']['queues']['consume_from']
        session = boto3.session.Session(
            profile_name=properties_['profile.name'])
        sqs_resource = session.resource(
            service_name=_SqsFifoQueue.SERVICE_NAME)
        sqs_queue = sqs_resource.Queue(url=queue_url)

        # Create the message factory.
        message_factory = messaging.factories.Message2()

        # Create the receiver factory.
        receiver_factory = _SqsFifoQueueReceiver(
            sqs_queue=sqs_queue,
            batch_size_maximum_count=properties_['message.receive.maximum.count'],
            wait_time_seconds=properties_['message.receive.wait.seconds'],
            message_factory=message_factory)

        # Create the deleter factory.
        deleter_factory = _SqsFifoQueueDeleter(sqs_queue=sqs_queue)

        # Create the queue abstract factory.
        queue_abstract_factory = _QueueAbstractFactory(
            sender_factory=sender_factory,
            receiver_factory=receiver_factory,
            deleter_factory=deleter_factory)

        return queue_abstract_factory

    def create_sender(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.producer.senders.Sender]
        """

        return self._sender_factory.create()

    def create_receiver(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.receivers.Receiver]
        """

        return self._receiver_factory.create()

    def create_deleter(self):

        """
        Returns
        -------
        typing.Type[clare.common.messaging.consumer.deleters.Deleter]
        """

        return self._deleter_factory.create()

    def __repr__(self):
        repr_ = ('{}('
                 'sender_factory={}, '
                 'receiver_factory={}, '
                 'deleter_factory={})')
        return repr_.format(self.__class__.__name__,
                            self._sender_factory,
                            self._receiver_factory,
                            self._deleter_factory)


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

        # Create the queue factory.
        queue_factory = _QueueAbstractFactory.new_sqs_fifo(
            properties=self._properties)

        # Create the room list watcher infrastructure.
        room_list_watcher_infrastructure = infrastructures.RoomListWatcher(
            sender=queue_factory.create_sender())

        # Create the download bot infrastructure.
        download_bot_infrastructure = infrastructures.DownloadBot(
            receiver=queue_factory.create_receiver(),
            deleter=queue_factory.create_deleter())

        # Create the application infrastructure.
        application_infrastructure = infrastructures.Application(
            room_list_watcher_infrastructure=room_list_watcher_infrastructure,
            download_bot_infrastructure=download_bot_infrastructure)

        return application_infrastructure

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
