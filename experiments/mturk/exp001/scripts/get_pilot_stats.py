#!/usr/bin/env python

import re
import os
import cPickle as pickle
import sys

sys.path.append("/Users/abe.kazemzadeh/proj/emo20q/emo20q-google-git/experiments/wsgi_archeology_for_peerj/")
dialog_dir = "/Users/abe.kazemzadeh/proj/emo20q/emo20q-google-git/experiments/wsgi_archeology_for_peerj/sessions/"


def dialog_iter(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        #print  subdir, dirs, files
        for filename in files:
            if re.match(r'^.+\.agent',filename ):
                yield filename


if __name__ == "__main__":
    for dialog_file in dialog_iter(dialog_dir):
        print dialog_file
        #import pdb; pdb.set_trace()
        obj = pickle.load(open(os.path.join(dialog_dir,dialog_file)))
        # for x in obj:
        #     if hasattr(x, 'text'):
        #         print x.text
        #     else:
        #         if hasattr(x,'q'):
        #             print x.q.text
        #         if hasattr(x,'q'):
        #             print x.a.text                    
        turns = [item for item in obj if hasattr(item, 'q')]
        print len(turns)
