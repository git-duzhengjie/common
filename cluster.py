def cluster_sum(cls_js, cls_key, js_info):
    clu_dict = {}
    for js in cls_js:
        my_key = []
        for key in cls_key:
            my_key.append(js_info[js][key])
        my_key = tuple(my_key)
        clu_dict[my_key] = clu_dict.setdefault(my_key, 0) + 1
    return clu_dict


def cluster_sum2(cls_key, js_info, tp):
    clu_dict = {}
    for js in js_info:
        my_key = []
        for key in cls_key:
            my_key.append(js_info[js][key])
        my_key = tuple(my_key)
        clu_dict[my_key][js_info[js][tp]] = clu_dict.setdefault(my_key, {}).setdefault(js_info[js][tp], 0) + 1
    return clu_dict


def cluster_list(cls_js, cls_key, cls_value):
    clu_dict = {}
    for js in cls_js:
        my_key = []
        for key in cls_key:
            my_key.append(cls_js[js][key])
        my_key = tuple(my_key)
        if cls_value == 'jinzuan':
            clu_dict.setdefault(my_key, []).append((js, cls_js[js]['jinzuan'], cls_js[js]['zuansi']))
        else:
            clu_dict.setdefault(my_key, []).append((js, cls_js[js][cls_value]))
    return clu_dict


def cluster_list2(cls_js, cls_key, js_info):
    clu_dict = {}
    for js in cls_js:
        my_key = []
        for key in cls_key:
            my_key.append(js_info[js][key])
        my_key = tuple(my_key)
        clu_dict.setdefault(my_key, []).append(js)
    return clu_dict