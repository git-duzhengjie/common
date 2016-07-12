# coding:utf-8
import os
import os.path
import shutil
import traceback

import re

import chardet


def get_file_dir(rp):
    ap = os.getcwd() + "/" + rp
    return os.listdir(ap)


def open_file(file_name):
    try:
        fp = open(file_name)
        return fp
    except IOError, e:
        print str(e)
        return None


def update_last_filetime(file_time):
    fp = open('config/last_file_time', 'w')
    fp.write(file_time)
    fp.close()


def dir_copy_tree(src, dst):
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    for name in names:
        src_name = os.path.join(src, name)
        dst_name = os.path.join(dst, name)
        if os.path.isdir(src_name):
            dir_copy_tree(src_name, dst_name)
        else:
            shutil.copy2(src_name, dst_name)


def copy_like(src, dst, like_name):
    if dst.__contains__(like_name):
        p_dir = re.split('%s\S*$' % like_name, dst)[0]
        if p_dir == "":
            files = os.listdir('.')
        else:
            files = os.listdir(p_dir)
        if dst.__contains__('/'):
            paths = dst.split('/')
        if dst.__contains__('\\'):
            paths = dst.split('\\')
        n = 0
        for i in range(len(paths)):
            if paths[i] == like_name:
                n = i
                break
        for fi in files:
            if fi.__contains__(like_name) and os.path.isdir(os.path.join(p_dir, fi)):
                shutil.copy(src, os.path.join('/'.join(paths[:n]), fi, '/'.join(paths[n+1:])))
    else:
        shutil.copy(src, dst)


def convert(filename, in_enc="GBK", out_enc="UTF8"):
    try:
        print "convert " + filename,
        content = open(filename).read()
        result = chardet.detect(content)
        coding = result.get('encoding')
        if coding != 'utf-8':
            print coding + " to utf-8!",
            new_content = content.decode(coding).encode(out_enc)
            open(filename, 'w').write(new_content)
            print " done"
        else:
            print coding
    except IOError:
        print " error"


def char_detect(string):
    import chardet
    return chardet.detect(string)



