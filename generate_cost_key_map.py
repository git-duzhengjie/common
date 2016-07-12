# coding:utf-8
import xml.etree.cElementTree as ET
import traceback
from util.dbholder import dbholder


def gm():
    try:
        branch = {}
        leaf = []
        leaf_n = {}
        tree = ET.ElementTree(file='config/constMapleaf.xml')
        for elem in tree.iter(tag='leaf'):
            leaf_n.setdefault(elem.attrib['id'], elem.attrib['name'])
        tree = ET.ElementTree(file='config/constMapTree.xml')
        for elem in tree.iter(tag='branch'):
            branch.setdefault(elem.attrib['id'], elem.attrib['name'])
        for elem in tree.iter(tag='node'):
            for ch_b in elem:
                for ch_l in ch_b:
                    if len(leaf) > 0 and ch_l.attrib['id'] not in zip(*leaf)[0]:
                        leaf.append(
                                [ch_l.attrib['id'], ch_b.attrib['id'], leaf_n.get(ch_l.attrib['id'], '').encode('utf-8'),
                                 branch.get(ch_b.attrib['id'], '').encode('utf-8')])
                    if len(leaf) == 0:
                        leaf.append(
                                [ch_l.attrib['id'], ch_b.attrib['id'], leaf_n.get(ch_l.attrib['id'], '').encode('utf-8'),
                                 branch.get(ch_b.attrib['id'], '').encode('utf-8')])
        # print(len(leaf), len(set(zip(*leaf)[0])))

        sql = "delete from raw_mid.key_map"
        conn = dbholder.getconn('raw_mid')
        conn.excute(sql)
        if len(leaf) > 0:
            conn.batch_excute(leaf, 100, conn.formatinsert('key_map', len(leaf[0])))

    except:
        traceback.print_exc()


gm()
