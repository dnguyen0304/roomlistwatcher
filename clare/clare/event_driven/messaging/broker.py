# -*- coding: utf-8 -*-


class Broker(object):

    def __init__(self, observable_factory):

        """
        Parameters
        ----------
        observable_factory : clare.event_driven.ObservableFactory
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
        subscriber : clare.event_driven.interfaces.INotifyable
        topic_name : str
        """

        observable = self._topic_index[topic_name]
        observable.register(observer=subscriber)

    def __repr__(self):
        repr_ = '{}(observable_factory={})'
        return repr_.format(self.__class__.__name__, self._observable_factory)
