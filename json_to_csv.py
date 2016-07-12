# coding:utf-8
# description:
# python version:
# version:v1.0
# author:杜政颉
# time:2016/6/30 12:00
# Copyright 成都简乐互动远景科技公司版权所有®


import json

from util.record import write_data


def json2csv(file_name):
    content_json = open(file_name).read()
    content = json.loads(content_json)
    keys = content['data']['rows'][0].keys()
    data = []
    for row in content['data']['rows']:
        line = []
        for k in keys:
            line.append(row.get(k, ''))
        data.append(line)
    write_data('json.csv', keys, data)


