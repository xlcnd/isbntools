# -*- coding: utf-8 -*-


class ISBNToolsException(Exception):
    """Base class for isbntools exceptions.

    This exception should not be raised directly,
    only subclasses of this exception should be used!

    However, you could use it to catch all errors defined
    by his subclasses.

    """

    def __str__(self):
        return getattr(self, 'message', '')  # pragma: no cover


class PluginNotLoadedError(ISBNToolsException):  # pragma: no cover
    """Exception raised when the plugin's loader doesn't load the plugin."""

    def __init__(self, path):
        self.message = "plugin (%s) wasn't loaded" % path
