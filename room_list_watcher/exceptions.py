# -*- coding: utf-8 -*-

from room_list_watcher.common import automation


class InitializationFailed(automation.exceptions.AutomationFailed):
    pass


class ExtractFailed(automation.exceptions.AutomationFailed):
    pass
