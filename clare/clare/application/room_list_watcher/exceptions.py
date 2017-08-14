# -*- coding: utf-8 -*-

from clare.common import automation


class InitializationFailed(automation.exceptions.ScrapeFailed):
    pass


class ExtractFailed(automation.exceptions.ScrapeFailed):
    pass
