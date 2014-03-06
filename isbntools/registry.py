#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wcat
import googlebooks


"""
Regestry for metadata services
"""
services = {'default': wcat.query,
            'wcat': wcat.query,
            'goob': googlebooks.query,
            'googlebooks': googlebooks.query
            }
