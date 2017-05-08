# -*- coding: utf-8 -*-

import abc
import json
import sys
import time

import enum

from . import exceptions
from .attempt import Attempt


class AutomatedEnum(enum.Enum):

    def __new__(cls):
        value = len(cls.__members__) + 1
        object_ = object.__new__(cls)
        object_._value_ = value
        return object_


class Topic(AutomatedEnum):
    ATTEMPT_STARTED = ()
    ATTEMPT_COMPLETED = ()


class IJsonSerializable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_json(self):

        """
        Returns
        -------
        str
        """

        pass


class AttemptStartedEvent(IJsonSerializable):

    topic = Topic.ATTEMPT_STARTED

    def __init__(self, attempt_number):

        """
        Parameters
        ----------
        attempt_number : int
        """

        self.arguments = {'attempt_number': attempt_number}

    def to_json(self):

        """
        Returns
        -------
        str
        """

        data = {'topic_name': self.topic.name, 'arguments': self.arguments}
        return json.dumps(data)

    def __repr__(self):
        repr_ = '{}(attempt_number={})'
        return repr_.format(self.__class__.__name__,
                            self.arguments['attempt_number'])


class AttemptCompletedEvent(IJsonSerializable):

    topic = Topic.ATTEMPT_COMPLETED

    def __init__(self, result, exception, next_wait_time):

        """
        Parameters
        ----------
        result : typing.Any
        exception : Exception
        next_wait_time : float
        """

        self.arguments = {'result': result,
                          'exception': exception,
                          'next_wait_time': next_wait_time}

    def to_json(self):

        """
        Returns
        -------
        str
        """

        data = {'topic_name': self.topic.name, 'arguments': self.arguments}
        return json.dumps(data)

    def __repr__(self):
        repr_ = '{}(result={}, exception={}, next_wait_time={})'
        return repr_.format(self.__class__.__name__,
                            self.arguments['result'],
                            self.arguments['exception'],
                            self.arguments['next_wait_time'])


class Policy(object):

    def __init__(self,
                 stop_strategies,
                 wait_strategy,
                 continue_strategies,
                 handled_exceptions,
                 messaging_broker):
        self._stop_strategies = stop_strategies
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies
        self._handled_exceptions = handled_exceptions
        self._messaging_broker = messaging_broker

    def execute(self, callable, _sleep=time.sleep):

        """
        Parameters
        ----------
        callable : callable
        _sleep : callable
            Used internally. Defaults to time.sleep.
        """

        attempt = Attempt.first()

        while True:
            attempt = next(attempt)
            attempt_number = attempt.number + 1
            was_successful = None
            result = None
            exception = None

            self.publish_attempt_started(attempt_number=attempt.number)

            try:
                attempt.result = callable()
            except self._handled_exceptions as handled_exception:
                attempt.was_successful = False
                attempt.exception = handled_exception
            else:
                attempt.was_successful = True

            should_continue = any(
                continue_strategy.should_continue(attempt=attempt)
                for continue_strategy
                in self._continue_strategies)

            for stop_strategy in self._stop_strategies:
                try:
                    stop_strategy.should_stop(attempt=attempt)
                except exceptions.MaximumRetry:
                    e = sys.exc_info()
                    should_stop = True
                    break
            else:
                should_stop = False

            should_wait = not attempt.was_successful and not should_stop
            wait_time = self._wait_strategy.compute_wait_time(attempt=attempt)

            self.publish_attempt_completed(result=result,
                                           exception=exception,
                                           next_wait_time=wait_time)

            if attempt.was_successful and not should_continue:
                break
            elif should_stop:
                raise e
            else:
                _sleep(wait_time)

        if attempt.was_successful:
            return attempt.result

    def publish_attempt_started(self, attempt_number):
        if self._messaging_broker is not None:
            event = AttemptStartedEvent(attempt_number=attempt_number)
            self._messaging_broker.publish(event=event.to_json(),
                                           topic_name=event.topic.name)

    def publish_attempt_completed(self, result, exception, next_wait_time):
        if self._messaging_broker is not None:
            event = AttemptCompletedEvent(result=result,
                                          exception=exception,
                                          next_wait_time=next_wait_time)
            self._messaging_broker.publish(event=event.to_json(),
                                           topic_name=event.topic.name)

    def __repr__(self):
        repr_ = ('{}('
                 'stop_strategies={}, '
                 'wait_strategy={}, '
                 'continue_strategies={}, '
                 'handled_exceptions={}, '
                 'messaging_broker={})')
        return repr_.format(self.__class__.__name__,
                            self._stop_strategies,
                            self._wait_strategy,
                            self._continue_strategies,
                            self._handled_exceptions,
                            self._messaging_broker)
