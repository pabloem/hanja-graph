import networkx as nx
import sys
import numpy as np
import scipy as sp
import csv

usage = """Usage:./ SynonymCorr.py synonymFile graphFile outFile"""

G = nx.read_graphml('crawlers/naver/data/basic_hanja_bipartite_26052015.graphml')
sts = nx.bipartite.sets(G)
A = nx.bipartite.biadjacency_matrix(G,sts[1])                                                               
A = A.astype('float')

k = 300

U, s, V = sp.sparse.linalg.svds(A,k)
nwA = sp.dot(U,np.diag(s))
nwA = sp.dot(nwA,V)
cors = np.corrcoef(nwA)

chars = list(sts[1])
chDic = {ch:i for i,ch in enumerate(chars)}

f = open(sys.argv[1])
outf = open(sys.argv[2],'w')
wr = csv.writer(outf)
rd = csv.reader(f)
for rw in rd:
    ch1 = chDic.get(rw[0])
    ch2 = chDic.get(rw[1])
    if None in [ch1, ch2]: continue
    wr.writerow(rw+[cors[ch1][ch2]])

f.close()
outf.close()
