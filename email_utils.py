# -*- coding: utf-8 -*-
"""
Send email util
"""
import os.path
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.utils import COMMASPACE


class EmailWrapper(object):

    def __init__(self, smtp_host, smtp_port, username, passwd,
                 from_addr, tls=False):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.passwd = passwd
        self.from_addr = from_addr
        self.tls = tls

    @property
    def server(self):
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        if self.tls:
            server.ehlo()
            server.starttls()
            server.ehlo()
        server.login(self.username, self.passwd)
        return server

    def sendmail(self, to_addrs, subject, text, text_type='html', files=[]):
        if isinstance(to_addrs, basestring):
            to_addrs = [to_addrs]

        msg = MIMEMultipart()
        msg['From'] = self.from_addr
        msg['To'] = COMMASPACE.join(to_addrs)
        msg['Subject'] = subject
        msg.attach(MIMEText(text, text_type))

        for f in files:
            att = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
            att.add_header('Content-Type', 'application/octet-stream')
            att.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(f))
            msg.attach(att)

        self.server.sendmail(self.from_addr, to_addrs, msg.as_string())


if __name__ == '__main__':
    wrapper = EmailWrapper('smtp.qq.com', 25, 'qq号', '密码',
                           'qq号@qq.com')
    wrapper.sendmail('to@qq.com', 'subject', 'content')
