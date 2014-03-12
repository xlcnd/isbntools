#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Exceptions for isbntools.dev

The classes in isbntools.dev should use the exceptions below.
"""


class ISBNToolsDevException(Exception):
    """ Base class for isbntools.dev exceptions

    This exception should not be raised directly,
    only subclasses of this exception should be used!
    """

    def __init__(self, msg=None):
        if msg:
            self.message = '%s (%s)' % (self.message, msg)

    def __str__(self):
        return getattr(self, 'message', '') # pragma: no cover


class WSHTTPError(ISBNToolsDevException):
    """ Exception raised for HTTP related errors
    """
    message = "an HTTP error has ocurred"


class WSURLError(ISBNToolsDevException):
    """ Exception raised for URL related errors
    """
    message = "an URL error has ocurred"


class WQDataNotFoundError(ISBNToolsDevException):
    """ Exception raised when there is no target data from the service
    """
    message = "the target data was not found"


class WQServiceIsDownError(ISBNToolsDevException):
    """ Exception raised when the service is not available
    """
    message = "the service is down (try later)"


class WPDataWrongShapeError(ISBNToolsDevException):
    """ Exception raised when the data hasn't the expected format
    """
    message = "the data hasn't the expected format"
