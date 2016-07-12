from util.my_string import *
from util.dbholder import DBHolder


dbholder = DBHolder()


def get_js_info(js_id, js_info_item):
    js_id_string = list2string(js_id)
    conn = dbholder.getconn('mid')
    js_info_item_string = ','.join(js_info_item)
    sql = "select %s,t1.js_id from (select * from js_distinct where js_id in (%s)) t1 left join raw_mid.js_map t2 on " \
          "t1.js_id=t2.js_id"
    result = conn.queryall(sql % (js_info_item_string, js_id_string))
    js_info = {}
    for res in result:
        info = {}
        for i in range(len(js_info_item)):
            value = res[i]
            if value is None:
                value = -1
            info.update({js_info_item[i]: value})
        js_info.setdefault(res[i+1], info)
    return js_info


def get_dv_info(dv_id, dv_info_item):
    dv_id_string = list2string(dv_id)
    conn = dbholder.getconn('mid')
    dv_info_item_string = ','.join(dv_info_item)
    sql = "select %s, t1.dv_id from (select * from dv_distinct where dv_id in (%s)) t1 left join raw_mid.dv_map t2 " \
          "on t1.dv_id=t2.dv_id"
    result = conn.queryall(sql % (dv_info_item_string, dv_id_string))
    dv_info = {}
    for res in result:
        info = {}
        for i in range(len(dv_info_item)):
            value = res[i]
            if value is None:
                value = -1
            info.update({dv_info_item[i]: value})
        dv_info.setdefault(res[i+1], info)
    return dv_info


def get_dv_js_info(dv_id, js_info_item, date=None):
    dv_id_string = list2string(dv_id)
    conn = dbholder.getconn('mid')
    js_info_item_string = ','.join(js_info_item)
    if date is not None:
        sql = "select %s, create_dv from (select t1.*, t2.js_str, t3.charge_total as daily_charge" \
          " from (select * from " \
          "js_distinct where create_dv in (%s)) t1 left join raw_mid.js_map t2 on t1.js_id=t2.js_id left join " \
          "(select * from dim.js_daily_charge where date = '%s') t3 on t1.js_id=t3.js_id) t"
        result = conn.queryall(sql % (js_info_item_string, dv_id_string, date))
    else:
        sql = "select %s, create_dv from (select t1.*,t2.js_str from (select * from " \
          "js_distinct where create_dv in (%s)) t1 left join raw_mid.js_map t2 on t1.js_id=t2.js_id) t"
        result = conn.queryall(sql % (js_info_item_string, dv_id_string))
    dv_info_js = {}
    for res in result:
        info = {}
        for i in range(len(js_info_item)):
            value = res[i]
            if value is None:
                value = 0
            info.update({js_info_item[i]: value})
        dv_info_js.setdefault(res[i+1], []).append(info)
    if 'daily_charge' in js_info_item:
        for dv in dv_info_js:
            dv_info_js[dv] = sorted(dv_info_js[dv], key=lambda x: x['daily_charge'], reverse=True)[0:10]
    if 'charge_total' in js_info_item:
        for dv in dv_info_js:
            dv_info_js[dv] = sorted(dv_info_js[dv], key=lambda x: x['charge_total'], reverse=True)[0:10]
    return dv_info_js
