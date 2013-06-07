# -*- coding: utf-8 -*-
"""
depends requests: https://github.com/kennethreitz/requests
"""

import Cookie

def cookie_to_dict(cookie):
    """Convert a string cookie into a dict"""
    cookie_dict = dict()
    C = Cookie.SimpleCookie(cookie)
    for morsel in C.values():
        cookie_dict[morsel.key] = morsel.value
    return cookie_dict

def dict_to_cookie(cookie_dict):
    """Convert a dict into a string cookie"""
    attrs = []
    for (key, value) in cookie_dict.items():
        attrs.append("%s=%s" % (key, value))
    return "; ".join(attrs)
