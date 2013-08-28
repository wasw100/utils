# -*- coding: utf-8 -*-

import urlparse

def get_values_by_name(url, name):
    """
    get url params's values by name
    """
    o = urlparse.urlparse(url)
    param_dict = urlparse.parse_qs(o.query)
    return param_dict.get(name)
    
    
if __name__ == "__main__":
    """test"""
    url = "http://www.codeif.com?s=python"
    print get_values_by_name(url, "s")
    print get_values_by_name(url, "t")