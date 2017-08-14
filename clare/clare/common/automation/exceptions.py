# -*- coding: utf-8 -*-


class ScrapeFailed(Exception):
    pass


class ConnectionLost(ScrapeFailed):
    pass


class ValidationFailed(ScrapeFailed):
    pass
