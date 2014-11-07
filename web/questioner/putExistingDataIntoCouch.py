#!/usr/bin/python


import sys
sys.path.append('/home/abe/emo20qgoogle/python') #update this for your own installation
from emo20q.data.base import HumanHumanTournament, HumanComputerTournament, Match, Turn
import time
import couchdb
db = couchdb.client.Database(url='http://ark.usc.edu:5984/emo20q')
import json
from uuid import uuid4
#doc_id = uuid4().hex


hh = HumanHumanTournament(annotationFile="../../annotate/emo20q.txt")
hc =  HumanComputerTournament(annotationFile="../../lists/onlineResults_2011-10-28.txt")

# note: currently human human dialogs have more data than human computer
# in the data sources that are currently being used
# the biggest difference is that human-computer dialogs don't have the surface
# question.  This needs to be addressed asap!

def match2JsonEncoder(x):
    out = {}
    if isinstance(x,Match):
        if x.type: out['type']=x.type
        if x.provenance: out['provenance'] = x.provenance
        out['events'] = [{'type':'Match', 'turns':x.turns()}] 
        #out['turns'] = []
        return out
    if isinstance(x,Turn):
        out['type'] = 'Turn'
        out['q'] = x.q
        out['qgloss'] = x.qgloss
        out['a'] = x.a
        out['agloss'] = x.agloss
        return {'type':'Turn','qa':[{'type':'Question','q':x.q,'qgloss':x.qgloss},
                                    {'type':'Answer','a':x.a,'agloss':x.agloss}] }
        #return {}

for m in hh.matches():
    m.type='dialog:human-human'
    m.provenance= ['xmpp','text','students','generation0']
    #create empty dialog in couch
    
    #print dir(m)
    
    #print json.dumps(m,sys.stdout,default=match2JsonEncoder,sort_keys=True, indent=2)
    #time.sleep(0.1)
    doc_id, doc_rev = db.save(json.loads(json.dumps(m,sys.stdout,default=match2JsonEncoder,sort_keys=True, indent=2)))
    print
    #    print t.qgloss
