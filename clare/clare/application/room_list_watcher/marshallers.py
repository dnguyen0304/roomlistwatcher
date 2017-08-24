# -*- coding: utf-8 -*-

import abc

import lxml.html


class Marshaller(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : typing.Any

        Returns
        -------
        object
        """

        raise NotImplementedError


class Nop(Marshaller):

    def marshall(self, object_):
        return object_

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class SeleniumWebElementToMessage(Marshaller):

    def __init__(self, message_factory):

        """
        Parameters
        ----------
        message_factory : clare.common.messaging.factories.Message2
        """

        self._message_factory = message_factory

    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : selenium.webdriver.remote.webelement.WebElement
        """

        html = object_.get_attribute('outerHTML')
        element = lxml.html.fragment_fromstring(html=html)
        room_path = element.get(key='href')
        message = self._message_factory.create()
        message.body = room_path
        return message

    def __repr__(self):
        repr_ = '{}(message_factory={})'
        return repr_.format(self.__class__.__name__, self._message_factory)
