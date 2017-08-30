# -*- coding: utf-8 -*-


class Message2(object):

    def __init__(self, id='', body='', delivery_receipt=''):

        """
        Parameters
        ----------
        id : str
            Unique identifier. Defaults to "".
        body : str
            Content. Defaults to "".
        delivery_receipt : str
            Unique identifier associated with the transaction of
            receiving this message. Defaults to "".
        """

        self.id = id
        self.body = body
        self.delivery_receipt = delivery_receipt

    def __repr__(self):
        repr_ = '{}(id="{}", body="{}", delivery_receipt="{}")'
        return repr_.format(self.__class__.__name__,
                            self.id,
                            self.body,
                            self.delivery_receipt)
