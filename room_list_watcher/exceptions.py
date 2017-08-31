# -*- coding: utf-8 -*-

from room_list_watcher.common import automation


class ScrapeFailed(automation.exceptions.AutomationFailed):
    pass


class InitializationFailed(ScrapeFailed):
    pass


class ExtractFailed(ScrapeFailed):
    pass
