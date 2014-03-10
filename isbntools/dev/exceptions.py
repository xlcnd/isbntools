#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Exceptions for isbntools.dev

The classes in isbntools.dev should use the exceptions below.
"""


class ISBNToolsException(Exception):
    """ Base class for isbntools.dev exceptions

    This exception should not be raised directly, 
    only subclasses of this exception should be used!
    """
    
    def __init__(self, msg=None):
        if msg:
            self.message = '%s (%s)' % (self.message, msg)
        
    def __str__(self):
        return getattr(self, 'message', '')


class WSHTTPError(ISBNToolsException):
    """ Exception raised for HTTP related errors 
    """
    message = "Error: an HTTP error has ocurred"
 
    
class WSURLError(ISBNToolsException):
    """ Exception raised for URL related errors
    """
    message = "Error: an URL error has ocurred"


class WQDataNotFoundError(ISBNToolsException):
    """ Exception raised when there is no target data from the service
    """
    message = "Error: the target data was not found"


class WQServiceIsDownError(ISBNToolsException):
    """ Exception raised when the service is not available
    """
    message = "Error: the service is down (try later)"


class WPDataWrongShapeError(ISBNToolsException):
    """ Exception raised when the data hasn't the expected format
    """
    message = "Error: the data hasn't the expected format"



#class NotValidMetadataError(ISBNToolsException):


