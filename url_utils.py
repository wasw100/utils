# -*- coding: utf-8 -*-

import urllib, urlparse

def get_values_by_name(url, name):
    """
    get url params's values by name
    """
    o = urlparse.urlparse(url)
    param_dict = urlparse.parse_qs(o.query)
    return param_dict.get(name)

def params_to_dict(params):
    """str params convert to dict"""
    if "?" not in params:
        params = "?%s" % params
    o = urlparse.urlparse(params)
    param_dict = urlparse.parse_qs(o.query)
    return param_dict

def dict_to_params(dict_data):
    """dict to url params"""
    return urllib.urlencode(dict_data, True)
    
if __name__ == "__main__":
    """test"""
    url = "http://www.codeif.com?s=python"
    print get_values_by_name(url, "s")
    print get_values_by_name(url, "t")

    dict_1 = dict(a="1", b='{"code":0}')

    #test params to dict
    params = dict_to_params(dict_1)
    print "params:", params
    dict_2 = params_to_dict(params)
    print "dict_2:", dict_2

    #dict to url params
    print "dict to params:", dict_to_params(dict_2)