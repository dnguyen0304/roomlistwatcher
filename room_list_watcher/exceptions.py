# -*- coding: utf-8 -*-

from room_list_watcher.common import automation


class InitializationFailed(automation.exceptions.ScrapeFailed):
    pass


class ExtractFailed(automation.exceptions.ScrapeFailed):
    pass
