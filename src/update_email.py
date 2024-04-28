#!/usr/bin/env python
import sys

def callback(data):
    email = data.email
    if email == b'rheactive@gmail.com':
        data.email = b'rhealacharya@gmail.com'
    return data

# Don't forget to include this line at the end
__filter__ = {"commit": callback}