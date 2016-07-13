# coding:utf-8
# description:
# python version:
# version:v1.0
# author:杜政颉
# time:2016/7/12 9:49
# Copyright 成都简乐互动远景科技公司版权所有®


from HTMLParser import HTMLParser

import re

from util.color import in_red


class HtmlParse(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('start tag:', tag)

    def handle_endtag(self, tag):
        print('end tag:', tag)

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        print('data:', data)

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def handle_image(self, src, alt, *args):
        pass

    def __del__(self):
        self.close()


def etl_html(start_tag, attr, value, html_string):
    result_html = ''
    html_string = html_string.rstrip()
    start_flag = False
    count = len(html_string)
    start_pattern = re.compile('<')
    end_pattern = re.compile('>')
    close_pattern = re.compile('/\S*>')
    i = 0
    tag_start = True
    while i < count:
        match = start_pattern.search(html_string[i:])
        if not match and i == 0:
            print(in_red(u'HTML字符串有误'))
            return None
        if match:
            start_pos = match.start()
        else:
            start_pos = 0
            tag_start = False
        print('start_pos:', i + start_pos)
        match = end_pattern.search(html_string[i + start_pos:])
        if not match:
            print(in_red(u'HTML字符串有误'))
            return None
        end_pos = match.start()
        match = close_pattern.match(html_string[start_pos:end_pos])
        if not tag_start and match:
            break
        this_tag = parse_tag(html_string[i + start_pos:i + end_pos])
        if this_tag and this_tag['tag'] == '!DOCTYPE':
            i = end_pos + 1
            continue
        if this_tag and this_tag['tag'] == start_tag and this_tag['attrib'][attr] == value:
            start_flag = True
        if start_flag:
            result_html += html_string[i:end_pos]
        i = i + end_pos + 1
    print(result_html)
    return result_html


def parse_tag(content):
    ct = content.split()
    tag_attr = {}
    for c in ct:
        if '=' not in c:
            tag_attr.setdefault('tag', c)
        else:
            c_ = c.split('=')
            tag_attr.setdefault('attr', {}).setdefault(c_[0], c_[1])
    return tag_attr


# parser = HtmlParse()
# parser.feed(open('../resources/huxiu.html').read())

with open('../resources/huxiu_n.html', 'w') as f:
    text = etl_html('div', 'class', 'login-reg-warp-modal', open('../resources/huxiu.html').read())
    if text:
        f.write(text)

