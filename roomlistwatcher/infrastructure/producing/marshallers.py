# -*- coding: utf-8 -*-

import abc
import re


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

    _OUTER_HTML_PATTERN = '<a href="(?P<room_path>/battle-[\d\w]+-[\d]+)" class="ilink">[\S\s]+</a>'

    def marshall(self, object_):

        """
        Parameters
        ----------
        object_ : selenium.webdriver.remote.webelement.WebElement

        Returns
        -------
        str

        Raises
        ------
        ValueError
            If the input could not be parsed.
        """

        html = object_.get_attribute('outerHTML')
        # XML parsing with xml.etree can't be used because it can't
        # handled malformed HTML such as those with mismatched tags.
        match = re.match(pattern=self._OUTER_HTML_PATTERN, string=html)
        if not match:
            template = 'The input "{html}" could not be parsed.'
            raise ValueError(template.format(html=html))
        # When the string matches the regex pattern, it is not possible
        # for this to raise a KeyError.
        room_path = match.groupdict()['room_path']
        return room_path

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
