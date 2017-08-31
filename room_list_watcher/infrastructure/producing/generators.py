# -*- coding: utf-8 -*-

import abc


class FilePathGenerator(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self):

        """
        Generate file paths.

        The values are evaluated lazily.

        Returns
        -------
        typing.Generator[str, None, None]
        """

        raise NotImplementedError
