# -*- coding: utf-8 -*-

import abc


class WebDriverDisposer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self, web_driver):

        """
        Garbage collect the resource.

        Parameters
        ----------
        web_driver : selenium.webdriver.remote.webdriver.WebDriver

        Returns
        -------
        None
        """

        raise NotImplementedError
