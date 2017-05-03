# -*- coding: utf-8 -*-

import abc


class IJsonSerializable(object):

    @abc.abstractmethod
    def to_json(self):

        """
        Returns
        -------
        str
        """

        pass
