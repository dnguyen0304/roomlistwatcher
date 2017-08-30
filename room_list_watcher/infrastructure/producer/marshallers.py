# -*- coding: utf-8 -*-

import abc

import lxml.html


class Marshaller(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def marshall(self, object_):

        """
        Convert from one type to another.

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


class SeleniumWebElementToString(Marshaller):

    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : selenium.webdriver.remote.webelement.WebElement

        Returns
        -------
        str
        """

        html = object_.get_attribute('outerHTML')
        element = lxml.html.fragment_fromstring(html=html)
        room_path = element.get(key='href')
        return room_path

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
