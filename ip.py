# coding:utf-8
#
# 该模块用于处理与IP相关的主题功能
# 包括查询ISP、city、其他信息等
#
import urllib2
import json
import socket
from util.color import *


socket.setdefaulttimeout(1)


def lookup_isp(ip):
    """

    :param ip: 查询的IP
    :return: IP的ISP（运营商）名
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            return data['data']['isp']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_city(ip):
    """

    :param ip: 查询的IP
    :return: IP对应的城市
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            return data['data']['city']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_detail(ip):
    """

    :param ip: 查询的IP
    :return: IP对应的国家、地区（西南、华中、华南、华北、华东、东北、西北）、省、市
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            data = data['data']
            return data['country'] + data['area'] + data['region'] + data['city']
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None


def lookup_all(ip):
    """

    :param ip: 查询的IP
    :return: IP所对应的所有信息
    """
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    try:
        sock = urllib2.urlopen(url, timeout=1)
        data = json.loads(sock.read())
        if data['code'] == 0:
            data = data['data']
            return data
        else:
            return None
    except urllib2.URLError, e:
        print "Url Error:", str(e)
        print in_red(url)
        return None
    except socket.timeout:
        print "Timed out!"
        return None
