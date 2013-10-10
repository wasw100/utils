# -*- coding: utf-8 -*-
"""
用于QQ登录的操作集合,步骤
1. http://check.ptlogin2.qq.com/check?uin...  
检查是否需要输入验证码 第一个变量为"0"则不需要,第二个变量为默认验证码,反之需要
2.get_p方法得到一个加密的p
3.get_p_url用户登录的url
"""

import hashlib
from utils import cookie_utils

def md5(origin):
    return hashlib.md5(origin).hexdigest().upper()

def get_g_tk(cookie):
    cookie_dict = cookie_utils.cookie_to_dict(cookie)
    skey = cookie_dict.get("skey")
    if skey:
        value = 5381
        for i in skey:
            value += (value<<5)+ord(i)
        return value & 0x7fffffff
    else:
        return None

def hexchar2bin(str_hex):
    result_bin = ''
    uin = str_hex.split('\\x')
    for i in uin[1:]:
        result_bin += chr(int(i, 16))
    return result_bin

def md5char2bin(str_md5):
    result_bin = ''
    for i in range(0, len(str_md5), 2):
        result_bin += chr(int(str_md5[i:i+2], 16))
    return result_bin

def get_p(password, code, c):
    """param code：check_vc方法返回的第二个变量或者输入的验证码"""
    password_md5 =  md5(password)
    passwd_bin = md5char2bin(password_md5)
    h = md5("%s%s" % (passwd_bin, hexchar2bin(c)))
    return md5("%s%s" % (h, code.upper()))

def get_p_url(qq, p, code):
    return "http://ptlogin2.qq.com/login?ptlang=2052&u=%s&p=%s&verifycode=%s&\
    css=http://imgcache.qq.com/ptcss/b2/sjpt/549000912/qzonelogin_ptlogin.css&\
    mibao_css=m_qzone&aid=549000912&u1=http%%3A%%2F%%2Fqzs.qq.com%%2Fqzone%%2Fv5%%2Floginsucc.html%%3Fpara%%3Dizone&ptredirect=1&\
    h=1&from_ui=1&dumy=&fp=loginerroralert&action=5-17-2972979&g=1&t=1&dummy=&js_type=2&js_ver=10009"\
     % (qq, p, code)

def clean_qq_cookie(cookie):
    """删除一些与qq登陆状态无用的cookie"""
    cookie_dict = cookie_utils.cookie_to_dict(cookie)
    clear_keys = ["ptcz", "verifysession", "superkey", "superuin", "RK", "_qz_referrer", "confirmuin", "ptuserinfo"]
    for clear_key in clear_keys:
        try:
            del cookie_dict[clear_key]
        except KeyError:
            pass
    return cookie_utils.dict_to_cookie(cookie_dict)
