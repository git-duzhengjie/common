# coding:utf-8
#
# 该模块处理与邮件相关的主题功能
# send_mail函数用于通过指定的邮件服务器向某邮箱发送邮件
#

import smtplib
import traceback
from email.mime.text import MIMEText


def send_mail(server_name, user, password, from_addr, to_addr, content, subject='waring'):
    """
    :param server_name:发送邮件服务器地址
    :param user:使用邮件服务器的用户名
    :param password:使用邮件服务器的密码
    :param from_addr:可以填写你希望出现在邮件中的发送者的名字
    :param to_addr:接受者的邮件地址
    :param content:邮件内容，支持HTML语法
    :param subject:邮件主题
    """
    try:
        if not isinstance(subject, unicode):
            subject = unicode(subject)
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        smtpobj = smtplib.SMTP()
        smtpobj.connect(server_name)
        smtpobj.login(user, password)
        smtpobj.sendmail(msg['from'], msg['to'], msg.as_string())
        print "Successfully sent email"
    except:
        print "Error: unable to send email"
        print traceback.format_exc()
