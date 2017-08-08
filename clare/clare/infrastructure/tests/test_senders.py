# -*- coding: utf-8 -*-

import httplib

import mock
from nose.tools import raises

from .. import senders
from clare.common.messaging import factories
from clare.common.messaging import producer


class TestSqsFifoQueue(object):

    def test_send(self):
        return_value = {
            'ResponseMetadata': {
                'HTTPStatusCode': httplib.OK
            }
        }
        sqs_queue = mock.Mock()
        sqs_queue.send_message = mock.Mock(return_value=return_value)

        message = factories.Message().create(body='foo')
        _message_group_id = 'foobar'

        sender = senders.SqsFifoQueue(sqs_queue=sqs_queue,
                                      _message_group_id=_message_group_id)
        sender.send(message)

        sqs_queue.send_message.assert_called_with(
            MessageBody=message.body,
            MessageGroupId=_message_group_id)

    @raises(producer.exceptions.SendTimeout)
    def test_send_http_error_raises_exception(self):
        return_value = {
            'ResponseMetadata': {
                'HTTPStatusCode': None
            }
        }
        sqs_queue = mock.Mock()
        sqs_queue.send_message = mock.Mock(return_value=return_value)

        message = factories.Message().create(body='foo')

        sender = senders.SqsFifoQueue(sqs_queue=sqs_queue)
        sender.send(message)
