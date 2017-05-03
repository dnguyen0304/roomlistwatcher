# -*- coding: utf-8 -*-

import abc


class IElementLookup(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_by_css_selector(self, css_selector):

        """
        Parameters
        ----------
        css_selector : str
            Equivalent to the CSS selector $("<css_selector>").

        Returns
        -------
        list
            Iterable collection of elements.
        """

        pass

    @abc.abstractmethod
    def find_by_class_name(self, class_name):

        """
        Parameters
        ----------
        class_name : str
            Equivalent to the CSS selector $(".<class_name>").

        Returns
        -------
        list
            Iterable collection of elements.
        """

        pass


class SeleniumDocument(IElementLookup):

    def __init__(self, web_driver):
        self._web_driver = web_driver

    def find_by_css_selector(self, css_selector):
        element = self._web_driver.find_element_by_css_selector(css_selector)
        return list(element)

    def find_by_class_name(self, class_name):
        element = self._web_driver.find_element_by_class_name(class_name)
        return list(element)
