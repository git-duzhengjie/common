# coding:utf-8
#
# 该模块用于处理与ftp相关的主题功能
# ftp_down函数用于下载指定ftp服务器指定目录下的指定文件
#

from ftplib import FTP
import os
import traceback
from util.timer import timer


def ftp_down(ftp_server, ftp_port, username, password, ftp_dir, filename):
    """
    :param ftp_server: ftp服务器ip
    :param ftp_port:ftp服务器端口
    :param username:登录用户名
    :param password:登录密码
    :param ftp_dir:进入ftp的目录
    :param filename:需要下载的文件名
    :return:
    """
    try:
        ftp = FTP()
        ftp.set_debuglevel(0)
        ftp.connect(ftp_server, ftp_port)
        ftp.login(username, password)
        ftp.cwd(ftp_dir)
        buffer_size = 1024
        file_handler = open(filename, 'wb')
        ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handler.write, buffer_size)
        ftp.set_debuglevel(0)
        file_handler.close()
        ftp.quit()
        print(timer.stop())
        return 'success'
    except:
        s = traceback.format_exc()
        return s


def ftp_up(ip, port, user, password, ftp_dir, filename):
    try:
        ftp = FTP()
        ftp.set_debuglevel(2)
        ftp.connect(ip, port)
        ftp.login(user, password)
        ftp.cwd(ftp_dir)
        bufsize = 1024
        file_handler = open(filename, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filename), file_handler, bufsize)
        ftp.set_debuglevel(0)
        file_handler.close()
        ftp.quit()
        print "ftp up OK"
        return True
    except:
        s = traceback.format_exc()
        print(s)
        return False


# ftp_down('120.26.204.52', '21', 'zhang', 'game80s@game3373.com', 'sjfxRead_rar',
#          'sjfxRead.2016052500-2016052523.rar')