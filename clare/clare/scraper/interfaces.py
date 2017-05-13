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


class IRepository(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, entity):

        """
        Parameters
        ----------
        entity : typing.Any

        Returns
        -------
        str
            Entity string ID.
        """

        pass

    @abc.abstractmethod
    def get(self, entity_id):

        """
        Parameters
        ----------
        entity_id : str

        Returns
        -------
        entity: typing.Any

        Raises
        ------
        EntityNotFound
            If the entity cannot be found.
        """

        pass
