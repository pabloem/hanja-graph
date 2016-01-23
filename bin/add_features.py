#!/usr/bin/env python3
import csv
import json
import sys
from collections import defaultdict

usage = "./add_rad_features.py res.csv newres.csv rads.json"

inf = open(sys.argv[1])
rd = csv.reader(inf)

outf = open(sys.argv[2],'w')
wr = csv.writer(outf)

rdf = open(sys.argv[3])
_rads = json.load(rdf)
rdf.close()

nw_f = ['share_radical','shared_radicals']
wr.writerow(next(rd)+nw_f)

def share_radical(h1,h2):
    sh1 = set() if h1 not in _rads else set(_rads[h1])
    sh2 = set() if h2 not in _rads else set(_rads[h2])
    return 1 if len(sh1.intersection(sh2)) > 0 else 0

def shared_radicals(h1,h2):
    sh1 = set() if h1 not in _rads else set(_rads[h1])
    sh2 = set() if h2 not in _rads else set(_rads[h2])
    return (len(sh1.intersection(sh2))/max(len(sh1)+0.0,len(sh2)+0.0,1.0))
            

shrd_rads = defaultdict(lambda : 0)

for i,rw in enumerate(rd):
    h1 = rw[1]
    h2 = rw[2]
    shrd = shared_radicals(h1,h2)
    shrd_rads[shrd] += 1
    wr.writerow(rw+[share_radical(h1,h2),shrd])
    pass

inf.close()
outf.close()
