#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def quiet_errors(exc_type, exc_value, traceback):
    """ An error format suitable for end user scripts 
    
        Usage: enter the following lines in your script
               from isbntools import quiet_errors
               sys.excepthook = quiet_errors
    """ 
    sys.stderr.write('Error: %s\n' % exc_value)
    


    
