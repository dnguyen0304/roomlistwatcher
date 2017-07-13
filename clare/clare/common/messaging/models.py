# -*- coding: utf-8 -*-


class Message(object):

    def __init__(self, body):

        """
        Parameters
        ----------
        body : str
        """

        self.body = body

    def __repr__(self):
        repr_ = '{}(body="{}")'
        return repr_.format(self.__class__.__name__, self.body)
