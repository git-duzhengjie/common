from __future__ import division


def getdivresultstring(v1, v2):
    if v1 != 0 and v2 != 0:
        return "%.2f%%" % (v1 / v2 * 100)
    else:
        return 0


def getdivresultreal(v1, v2):
    if v1 != 0 and v2 != 0:
        return "%.4f" % (v1 / v2)
    else:
        return 0


def difset(set1, set2):
    ret_set = {}
    for i in set2:
        if i in set1:
            continue
        ret_set[i] = 1
        set1[i] = 1
    return ret_set


def set2string(set):
    reval = []
    ret = ""
    if len(set) == 0:
        return ret
    for i in set:
        tmp = "\'%s\'" % i
        reval.append(tmp)
    return ','.join(reval)


def genset(rs, key_idx, store_value=True):
    ret_set = {}
    rs_len = len(rs)
    for i in range(rs_len):
        rec = rs[i]
        key = rec[key_idx]
        if key not in ret_set:
            if store_value:
                ret_set[key] = []
            else:
                ret_set[key] = 1
        if store_value:
            ret_set[key].append(rec)
    return ret_set


def c(n1,n2):
    n = 1
    n22 = 1
    for i in range(n2):
        n *= n1-i
    for i in range(n2):
        n22 *= i+1
    return int(n/n22)

