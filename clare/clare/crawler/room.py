# -*- coding: utf-8 -*-


class Room(object):

    def __init__(self, is_empty, has_replay):
        self.is_empty = is_empty
        self.has_replay = has_replay

    @classmethod
    def from_document(cls, document):

        """
        Parameters
        ----------
        document : clare.crawler.documents.IElementLookup
        """

        css_selector = 'body a.roomtab.button.cur.closable span'
        elements = document.find_by_css_selector(css_selector)
        # Is the text attribute in lxml equivalent to the innerHTML
        # property in JavaScript?
        is_empty = elements[0].text == '(empty room)' if elements else None

        class_name = 'replayDownloadButton'
        elements = document.find_by_class_name(class_name)
        has_replay = elements[0] is not None if elements else None

        room = cls(is_empty=is_empty, has_replay=has_replay)

        return room

    def __repr__(self):
        repr_ = '{}(is_empty={}, has_replay={})'
        return repr_.format(self.__class__.__name__,
                            self.is_empty,
                            self.has_replay)
