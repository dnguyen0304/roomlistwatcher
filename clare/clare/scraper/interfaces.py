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
        collections.Sequence
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
        collections.Sequence
        """

        pass
