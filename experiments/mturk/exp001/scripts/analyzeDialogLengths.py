#!/usr/bin/python

import json
import sys

datafile = "emo20q_webdata_fromCouch_20121102.json"

data = json.load(open(datafile))

print "\t".join(["exp","wave","emotion","success","difficulty","length"])
for x in data['rows']:
    if 'type' in x['doc']:
        if  x['doc']['type'] == 'Dialog':
            dialog= x['doc']
            if 'success' not in dialog['param']:
                continue
            if 'exp' not in dialog['param']:
                continue
            exp     = dialog['param']['exp']
            wave    = dialog['param']['wave']
            success = dialog['param']['success']
            emotion = dialog['param']['emotion']
            length  = len([x for x in dialog['container'] if 'type' in x if x['type'] == "Turn"]) 
            print "\t".join([str(x) for x in [exp, wave, emotion, success, length]])

