# -*- coding: utf-8 -*-

import lxml.html


class Nop(object):

    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : typing.Any
        """

        return object_

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class SeleniumWebElementToMessage(object):

    def __init__(self, message_factory):

        """
        Parameters
        ----------
        message_factory : clare.common.messaging.factories.MessageFactory
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
        message = self._message_factory.create(body=room_path)
        return message

    def __repr__(self):
        repr_ = '{}(message_factory={})'
        return repr_.format(self.__class__.__name__, self._message_factory)
