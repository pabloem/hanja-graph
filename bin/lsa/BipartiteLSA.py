#!/usr/bin/env python3

import networkx as nx
import networkx.algorithms as nxa
import sys
import numpy as np
import scipy as sp
import heapq
import csv

usage = """Usage: ./BipartiteLSA gf.graphml outf [-w] [k]"""

if len(sys.argv) < 2:
    print(usage)
    sys.exit(0)

argc = 1
inf = sys.argv[argc]
argc += 1

outf = sys.argv[argc]
argc+=1

weight = False
if len(sys.argv) > argc and sys.argv[argc] == '-w':
    weight = True
    argc += 1

k = 800
if len(sys.argv) > argc:
    k = int(sys.argv[argc])
    argc += 1

#G = nx.read_graphml('graphs/basic_hanja_bipartite_26052015.graphml')
G = nx.read_graphml(inf)
sts = nx.bipartite.sets(G)

A = nx.bipartite.biadjacency_matrix(G,sts[1])                                                               
A = A.astype('float')

U, s, V = sp.sparse.linalg.svds(A,k)
nwA = sp.dot(U,np.diag(s))
nwA = sp.dot(nwA,V)

cors = np.corrcoef(nwA)
for i in range(cors.shape[0]):
    cors[i,i] = 0

q = []
for i,rw in enumerate(cors):
    for j, elm in enumerate(rw):
        if j <= i: continue
        heapq.heappush(q,(elm,i,j))

chars = list(sts[1])

outf = "testitou"
of = open(outf,'w')
wr = csv.writer(of)
tops = heapq.nlargest(500,q)
sentcol = set()
for corr,i1,i2 in tops:
    wr.writerow([chars[i1],chars[i2],i1,i2])

of.close()
