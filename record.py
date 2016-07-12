# -*- coding: utf-8 -*-'
import json

from util.csvfd import CSV


def write_data(my_file, head, data):
    csvfile = CSV(my_file, 'w')
    if head != "":
        csvfile.wrow(head)
    csvfile.wrows(data)
    csvfile.close()


def write_m_data(my_file, head, data):
    csvfile = CSV(r'res/' + my_file, 'w')
    if head != "":
        csvfile.wrows(head)
    csvfile.wrows(data)
    csvfile.close()


def write_csv(data):
    csvfile = CSV('tmp', 'w')
    csvfile.wrows(data)
    csvfile.close()


def write_tsv(data):
    fp = open('tmp', 'w')
    for da in data:
        fp.write('\t'.join(str(d) for d in da).replace('\\\"', '\\\\\"') + '\n')
    fp.close()
