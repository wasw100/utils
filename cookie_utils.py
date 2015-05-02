# -*- coding: utf-8 -*-
"""
depends requests: https://github.com/kennethreitz/requests
"""
import requests.cookies
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


def get_value_by_name(cookie, name):
    """get cookie value by name from a string cookie"""
    cookie_dict = cookie_to_dict(cookie)
    return cookie_dict.get(name)


def get_requests_session(cookies, referer=None, ua=None):
    """Returns a requests.Session with cookie
    :param cookies: cookie_str, eg. a=1; b=2
    """
    session = requests.Session()
    if referer:
        session.headers['Referer'] = 'http://i.qq.com/'
    if ua:
        session.headers['User-Agent'] = ua

    if cookies:
        cookie_dict = cookie_to_dict(cookies)
        session.cookies = requests.cookies.cookiejar_from_dict(cookie_dict)

    # 调试的时候可以打开代理
    # session.proxies = {'http': 'http://127.0.0.1:8888/',
    #                    'https': 'http://127.0.0.1:8888/'}

    return session


def get_httpclient_cookie(response, request=None):
    """
    Returns cookie string by tonado AsyncHTTPClient's request and response
    :param request: class:tornado.httpclient.HTTPRequest
    :param response: class:tornado.httpclient.HTTPResponse
    """
    cookiejar = requests.cookies.RequestsCookieJar()

    if request is None:
        request = response.request

    request_cookie = request.headers.get("Cookie")
    if request_cookie:
        if type("") != type(request_cookie):
            request_cookie = request_cookie.encode("utf-8")
        cookie_dict = cookie_to_dict(request_cookie)
        requests.cookies.cookiejar_from_dict(cookie_dict, cookiejar)

    for sc in response.headers.get_list("Set-Cookie"):
        C = Cookie.SimpleCookie(sc)
        for morsel in C.values():
            cookie = requests.cookies.morsel_to_cookie(morsel)
            cookiejar.set_cookie(cookie)
    cookie_dict = cookiejar.get_dict(path="/")
    return dict_to_cookie(cookie_dict)
