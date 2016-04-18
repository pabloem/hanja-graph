#!/usr/bin/python3
import networkx as nx
import networkx.algorithms as nxa
import sys
import numpy as np
import scipy as sp
import heapq
import csv

usage = """"Usage: ./DoLSA.py gf.graphml outf [-w] [k]
\t- k - Number of singular values to compute
"""
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

k = 3
if len(sys.argv) > argc:
    k = int(sys.argv[argc])
    argc += 1

G = nx.read_graphml(inf)

# We remove nodes with no edges
degs = list(nx.degree(G).items())
zerdegs = [a for a in degs if a[1] == 0]
for nd,deg in zerdegs:
    G.remove_node(nd)

chars = [it[1]['chinese'] if 'chinese' in it[1] else it[0] for it in G.node.items()]

A = nx.adjacency_matrix(G)

A = A.astype('float')
U, s, V = sp.sparse.linalg.svds(A,k)

nwlen = U.shape[0]
#snw = np.resize(s,nwlen)
#snw[[i for i in range(s.shape[0],nwlen)]]

nwA = sp.dot(U,np.diag(s))
nwA = sp.dot(nwA,V) # Adding pseudocount
dim = nwA.shape[0]


probrows = set()
### Adding the weighting by log
probcnt = 0
if weight:
    colsums = nwA.sum(axis=1)
    rowsums = nwA.sum(axis=0)
    with np.errstate(invalid='raise'):
        for i, rw in enumerate(nwA):
            for j, val in enumerate(rw):
                try:
                    #if rowsums[i] <= 0: 
                    #    nwA[i][j] = 0
                    #    probrows.add((i,j))
                    #    continue
                    nwA[i][j] = val/rowsums[j]*np.log2([dim/colsums[i]])[0]
                except:
                    print("Error")
                    probcnt += 1
                    raise
                    #print(dim)
                    #print(rowsums[i])

cors = np.corrcoef(nwA)
for i in range(cors.shape[0]):
    cors[i,i] = 0

"""
q = []
for i, rw in enumerate(cors):
    maxel = nanargmax(rw)[0]
    heapq.heappush(q,(cors[i][maxel],i,j))
"""

q = []
for i,rw in enumerate(cors):
    for j, elm in enumerate(rw):
        if j <= i: continue
        if (i,j) in probrows or (j,i) in probrows: continue
        heapq.heappush(q,(elm,i,j))

of = open(outf,'w')
wr = csv.writer(of)
tops = heapq.nlargest(500,q)
sentcol = set()
for corr,i1,i2 in tops:
    #if (i1,i2) in probrows: continue
    #if i1 in sentcol or i2 in sentcol: continue
    #sentcol.add(i1)
    #sentcol.add(i2)
    wr.writerow([chars[i1],chars[i2],i1,i2])

of.close()

#clA = U*s*V
