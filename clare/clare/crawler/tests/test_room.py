# -*- coding: utf-8 -*-

from lxml import cssselect, etree
from nose.tools import assert_equal, assert_false, assert_is_none, assert_true

from ..document import IElementLookup
from ..room import Room


class MockDocument(IElementLookup):

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


class TestMockDocument(object):

    def __init__(self):
        self.document = None

    def setup(self):
        string = """
<head>
  <div class="foo">Foo</div>
  <div class="bar">Bar</div>
</head>"""
        self.document = MockDocument.from_string(string)

    def test_find_by_css_selector(self):
        css_selector = '.foo'
        elements = self.document.find_by_css_selector(css_selector)
        assert_equal(len(elements), 1)
        assert_equal(elements[0].attrib['class'], 'foo')

    def test_find_by_class_name(self):
        class_name = 'foo'
        elements = self.document.find_by_class_name(class_name)
        assert_equal(len(elements), 1)
        assert_equal(elements[0].attrib['class'], 'foo')


class TestRoom(object):

    def test_from_document_is_empty(self):
        string = """
<body>
  <a class="roomtab button cur closable">
    <span>(empty room)</span>
  </a>
</body>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_true(room.is_empty)
        assert_is_none(room.has_replay)

    def test_from_document_is_not_empty(self):
        string = """
<body>
  <a class="roomtab button cur closable">
    <span></span>
  </a>
</body>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_false(room.is_empty)
        assert_is_none(room.has_replay)

    def test_from_document_has_replay(self):
        string = """<a class="replayDownloadButton"></a>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_is_none(room.is_empty)
        assert_true(room.has_replay)

    def test_from_document_does_not_have_replay(self):
        string = """<a class="foo"></a>"""
        document = MockDocument.from_string(string)
        room = Room.from_document(document)
        assert_is_none(room.is_empty)
        assert_false(room.has_replay)
