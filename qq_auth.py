# -*- coding: utf-8 -*-
"""
tornado中使用QQ登陆认证
具体使用参考以及示例代码torndo.auth.FacebookGraphMixin的注释
"""

from __future__ import absolute_import, division, print_function, with_statement

import re

from tornado import httpclient, escape
from tornado.auth import _auth_return_future, AuthError, OAuth2Mixin

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    import urllib.parse as urllib_parse  # py3
except ImportError:
    import urllib as urllib_parse  # py2

class QQGraphMixin(OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = "https://graph.qq.com/oauth2.0/token?"
    _OAUTH_AUTHORIZE_URL = "https://graph.qq.com/oauth2.0/authorize?"
    _OAUTH_NO_CALLBACKS = False
    _QQ_BASE_URL = "https://graph.qq.com"

    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        fields = set(["nickname", "gender", 'figureurl'])
        if extra_fields:
            fields.update(extra_fields)
        http.fetch(self._oauth_request_token_url(extra_params=dict(grant_type="authorization_code"), **args),
                   self.async_callback(self._on_access_token, redirect_uri, client_id,
                                       client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('QQ auth error: %s' % str(response)))
            return

        args = escape.parse_qs_bytes(escape.native_str(response.body))
        session = {
            "access_token": args["access_token"][0],
            "expires": args.get("expires_in")[0]
        }
        
        http = self.get_auth_http_client()
        http.fetch("https://graph.qq.com/oauth2.0/me?access_token="+session["access_token"], 
                   self.async_callback(self._on_access_openid, redirect_uri, client_id,
                                       client_secret, session, future, fields))

        
    def _on_access_openid(self, redirect_uri, client_id, client_secret, session,
                         future, fields, response):
        
        if response.error:
            future.set_exception(AuthError('QQ auth error: %s' % str(response)))
            return
        m = re.search(r'"openid":"([a-zA-Z0-9]+)"', escape.native_str(response.body))

        session["openid"] = m.group(1)

        self.qq_request(
            path="/user/get_user_info",
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session["access_token"],
            oauth_consumer_key=client_id,
            openid=session["openid"]
        )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update(session)
        future.set_result(fieldmap)

    @_auth_return_future
    def qq_request(self, path, callback, access_token=None, client_id=None, open_id=None,
                         post_args=None, **args):
        url = self._QQ_BASE_URL + path
        all_args = {
                    "access_token": access_token,
                    "oauth_consumer_key": client_id,
                    "open_id": open_id,
                    }
            
        all_args.update(args)

        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
        callback = self.async_callback(self._on_qq_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_qq_request(self, future, response):
        if response.error:
            future.set_exception(AuthError("Error response %s fetching %s" %
                                           (response.error, response.request.url)))
            return

        future.set_result(escape.json_decode(response.body))

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()
