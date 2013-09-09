# -*- coding: utf-8 -*-
"""
测试tornado使用QQ登陆的模块qq_auth
在http://connect.qq.com/intro/login申请QQ登陆的app id和app key
修改下面对应的参数,直接在当前目录下运行: python qq_auth_test.py
"""
import sys
sys.path.append("..")

import qq_auth
import tornado.ioloop
import tornado.web
import tornado.gen

class QQGraphLoginHandler(tornado.web.RequestHandler, qq_auth.QQGraphMixin):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        redirect_uri = "http://{域名}/auth/qqgraph"
        code = self.get_argument("code", False)
        if code:
            user = yield self.get_authenticated_user(
                  redirect_uri=redirect_uri,
                  client_id=self.settings["qq_api_key"],
                  client_secret=self.settings["qq_secret"],
                  code=self.get_argument("code"))
            self.finish(user)
        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings["qq_api_key"],
                extra_params=dict(response_type="code"))

def main():
    setting = dict(
                    qq_api_key = "{你申请的app id}",
                    qq_secret = "{你申请的app key}"
                   )
    application = tornado.web.Application([(r"/auth/qqgraph", QQGraphLoginHandler),], **setting)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()