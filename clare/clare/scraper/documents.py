# -*- coding: utf-8 -*-

from lxml import cssselect, etree

from . import interfaces


class LXmlDocument(interfaces.IElementLookup):

    def __init__(self, element_tree):
        self._element_tree = element_tree

    @classmethod
    def from_string(cls, string):
        parser = etree.HTMLParser()
        element_tree = etree.fromstring(string, parser=parser)
        document = cls(element_tree=element_tree)
        return document

    def find_by_css_selector(self, css_selector):
        apply_css_selector = cssselect.CSSSelector(css=css_selector,
                                                   translator='html')
        elements = apply_css_selector(self._element_tree)
        return elements

    def find_by_class_name(self, class_name):
        css_selector = '.' + class_name
        elements = self.find_by_css_selector(css_selector)
        return elements
