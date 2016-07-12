# --*--coding:utf-8--*--
import hashlib
import socket
import struct
import time
from util.time_utility import *
from util.readstate import read_run_model
from util.file import get_file_dir


def str2dict(string):
    str_list = string.split(';')
    str_dict = {}
    for str_l in str_list:
        tmp = str_l.split(':')
        str_dict.setdefault(tmp[0], tmp[1])
    return str_dict


def key2string(dt):
    re_str = ""
    sort_key = sorted(dt)
    for key in sort_key:
        value = ""
        if dt[key] is not None:
            value = str(dt[key][0])
        re_str += str(key) + "=" + value + "&"
    return re_str.rstrip('&').lower()


def ip2long(ip_string):
    ip = socket.inet_aton(ip_string)
    return struct.unpack("!L", ip)[0]


def long2ip(ip_long):
    ip = socket.htonl(ip_long)
    return socket.inet_ntoa(struct.pack('I', ip))


def dev_format(mac, idfa):
    run_model = read_run_model()
    if run_model == 1:
        mac = mac.replace(':', '').replace('.', '').replace('-', '').lower()
        idfa = idfa.replace(':', '').replace('.', '').replace('-', '').replace('\\', '').replace('_', '').lower()
        if len(idfa) != 32:
            idfa = '00000000000000000000000000000000'
    if run_model == 2:
        mac = mac.replace(':', '').replace('.', '').replace('-', '').lower()
        idfa = idfa.replace(':', '').replace('.', '').replace('-', '').replace('\\', '').replace('_', '').lower()
    return mac + ' ' + idfa


def str2time(str_time):
    int_time = int(str_time)
    float_time = int_time/1000.0
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float_time))


def list2string(lt_ar):
    if len(lt_ar) == 0:
        return '0'
    return ','.join(str(lt) for lt in lt_ar)


def logkey(key):
    return "\"logkey\":\"%s\"" % key


def get_ftp_filename(date):
    date = date.replace('-', '')
    return 'sjfxRead.' + date + '00-' + date + '23.rar'


def rm_exception(string):
    return string.split(' ')[0].replace('%', '').replace('(', '').replace(')', '').replace('\\', '')


def get_select_string(cube):
    select_string = ''
    if 'serverid' in cube:
        select_string += 'ifnull(serverid, -1) as serverid,'
    elif 'register_server' in cube:
        select_string += 'ifnull(register_server, -1) as serverid,'
    else:
        select_string += '0 as serverid,'
    if 'channel' in cube:
        select_string += 'ifnull(channel, -1) as channel,'
    else:
        select_string += '0 as channel,'
    if 'ptid' in cube:
        select_string += 'ifnull(ptid, -1) as ptid,'
    else:
        select_string += '0 as ptid,'
    return select_string


def get_start_end():
    fp = open('config/last_file_time', 'r')
    ln = fp.readline().strip()
    fp.close()
    if ln == "":
        return None
    last_file_time = ln
    current_time = now_hour()
    n = gethours(last_file_time, current_time)
    file_time = last_file_time
    suffix = '.gz'
    break_flag = False
    for i in range(n):
        file_name = file_time + suffix
        file_list = get_file_dir('log/sjfxRead')
        if file_name not in file_list:
            break_flag = True
            break
        if break_flag:
            break
        file_time = addhour2(file_time, 1)
    if last_file_time == file_time:
        return None
    else:
        fp = open('config/last_file_time', 'w')
        fp.write(file_time)
        fp.close()
        return [last_file_time, file_time, get_date_from_hour(last_file_time),
                get_date_from_hour(addhour2(file_time, -1))]



