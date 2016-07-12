import json
from util.dbholder import dbholder


def load():
    fp = open('config/agentAndPtConfig.json')
    json_data = fp.readlines()
    data = json.loads(''.join(json_data).strip('\n'))
    ar = []
    for sk in data[0]['children']:
        for tk in sk['children']:
            ar.append([sk['val'], tk['val'], sk['text'].encode('utf-8') + ' ' + tk['text'].encode('utf-8')])
        ar.append([sk['val'], 0, sk['text'].encode('utf-8')])
    conn = dbholder.getconn('raw_mid')
    conn.insert_data(ar, 'channel_map')

load()