# -*- coding: utf-8 -*-

from . import interfaces


class NoDuplicate(interfaces.IFilterStrategy):

    def __init__(self, seen_paths):

        """
        Parameters
        ----------
        seen_paths : collections.Container
        """

        self._seen_paths = seen_paths

    def should_filter(self, path):
        if path in self._seen_paths:
            should_filter = True
        else:
            should_filter = False
        return should_filter

    def __repr__(self):
        repr_ = '{}(seen_paths={})'
        return repr_.format(self.__class__.__name__, self._seen_paths)
