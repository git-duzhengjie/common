import urllib2
import socket


socket.setdefaulttimeout(1)


def post(url, values):
    try:
        data = urllib2.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return response.read()
    except urllib2.URLError, e:
        print("Url Error:", str(e))
        return None
    except socket.timeout:
        print('request timeout')
        return None


def get(url):
    try:
        return urllib2.urlopen(url).read()
    except urllib2.URLError, e:
        print("Url Error:", str(e))
        return None
    except socket.timeout:
        print('request timeout')
        return None

