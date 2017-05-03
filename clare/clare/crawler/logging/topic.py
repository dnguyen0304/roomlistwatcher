# -*- coding: utf-8 -*-

import enum


class AutomatedEnum(enum.Enum):

    def __new__(cls):
        value = len(cls.__members__) + 1
        object_ = object.__new__(cls)
        object_._value_ = value
        return object_


class Topic(AutomatedEnum):
    PAGE_DOWNLOADED = ()
