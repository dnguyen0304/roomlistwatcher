# -*- coding: utf-8 -*-

import abc
import sys
import time

from . import exceptions
from .attempt import Attempt


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


class INotifyable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def notify(self, event):

        """
        Parameters
        ----------
        event : clare.retry.policy.IJsonSerializable

        Returns
        ------
        None
        """

        pass


class Observable(INotifyable):

    def __init__(self):
        self._observers = set()

    def register(self, observer):

        """
        Parameters
        ----------
        observer : clare.retry.policy.INotifyable
        """

        self._observers.add(observer)

    def notify(self, event):

        """
        Parameters
        ----------
        event : clare.retry.policy.IJsonSerializable
        """

        for observer in self._observers:
            observer.notify(event=event)

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class ObservableFactory(object):

    def build(self):

        """
        Returns
        ----------
        clare.retry.policy.INotifyable
        """

        observable = Observable()
        return observable


class Broker(object):

    def __init__(self, observable_factory):

        """
        Parameters
        ----------
        observable_factory : clare.retry.policy.ObservableFactory
        """

        self._observable_factory = observable_factory
        self._topic_index = dict()

    def create_topic(self, name):

        """
        A new topic is created only if one by the same name does not
        already exist.

        Parameters
        ----------
        name : str
        """

        if name not in self._topic_index:
            self._topic_index[name] = self._observable_factory.build()

    def list_topics(self):

        """
        Returns
        -------
        collections.Sequence
        """

        return self._topic_index.keys()

    def publish(self, event, topic_name):

        """
        Parameters
        ----------
        event : clare.retry.policy.IJsonSerializable
        topic_name : str
        """

        observable = self._topic_index[topic_name]
        observable.notify(event=event)

    def subscribe(self, subscriber, topic_name):

        """
        Parameters
        ----------
        subscriber : clare.retry.policy.INotifyable
        topic_name : str
        """

        observable = self._topic_index[topic_name]
        observable.register(observer=subscriber)

    def __repr__(self):
        repr_ = '{}(observable_factory={})'
        return repr_.format(self.__class__.__name__, self._observable_factory)


class Policy(object):

    def __init__(self,
                 stop_strategies,
                 wait_strategy,
                 continue_strategies,
                 handled_exceptions,
                 pre_hooks,
                 post_hooks):
        self._stop_strategies = stop_strategies
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies
        self._handled_exceptions = handled_exceptions
        self._pre_hooks = pre_hooks
        self._post_hooks = post_hooks

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

            self._call_pre_hooks(attempt_number=attempt.number)

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

            self._call_post_hooks(result=result,
                                  exception=exception,
                                  wait_time=wait_time)

            if attempt.was_successful and not should_continue:
                break
            elif should_stop:
                raise e
            else:
                _sleep(wait_time)

        if attempt.was_successful:
            return attempt.result

    def _call_pre_hooks(self, attempt_number):
        context = {'attempt_number': attempt_number}
        for pre_hook in self._pre_hooks:
            pre_hook(context)

    def _call_post_hooks(self, result, exception, wait_time):
        context = {'result': result,
                   'exception': exception,
                   'next_wait_time': wait_time}
        for post_hook in self._post_hooks:
            post_hook(context)

    def __repr__(self):
        repr_ = ('{}('
                 'stop_strategies={}, '
                 'wait_strategy={}, '
                 'continue_strategies={}, '
                 'handled_exceptions={}, '
                 'pre_hooks={}, '
                 'post_hooks={})')
        return repr_.format(self.__class__.__name__,
                            self._stop_strategies,
                            self._wait_strategy,
                            self._continue_strategies,
                            self._handled_exceptions,
                            self._pre_hooks,
                            self._post_hooks)
