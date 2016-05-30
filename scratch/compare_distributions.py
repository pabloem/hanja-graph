import networkx as nx
import numpy as np
import scipy as sp
import csv
import time


G = nx.read_graphml('graphs/bipartite_graph.graphml')
output_dir = "tmpDistancesFull"

sts = nx.bipartite.sets(G)

words = None
hanjas = None
if len(sts[0]) > 6000: 
    words = sts[0]
    hanjas = sts[1]
else: 
    words = sts[1]
    hanjas = sts[0]

wordic = {e:k for k,e in enumerate(words)}

synonyms = None
with open('data/synonyms.csv') as f:
    rd = csv.reader(f)
    synonyms = rd.readrows()

synDP = []
randDP = []

A = nx.bipartite.biadjacency_matrix(G,hanjas)
A.dtype = float

minK = 200
maxK = 3400

for k in range(minK,maxK,200):
    st = time.clock()
    print("Factorizing for k={}".format(k))
    U,s,V = sp.sparse.linalg.svds(A,k)
    Vtr = V.transpose()

    print("Factorized. Obtaining distribution.")
    for pr in synonyms:
        c1 = pr[0]
        c2 = pr[1]
        v1 = Vtr[wordic[c1]]
        v2 = Vtr[wordic[c2]]
        synDP.append([np.dot(v1,v2),c1,c2])

    for _ in synonyms:
        v1 = choice(Vtr)
        v2 = choice(Vtr)
        randDP.append(np.dot(v1,v2))

    del U
    del s
    del V
    end = time.clock()
    print("Saving. Took {} seconds for k={}".format(end-st,k))
    with open("{}/randdist_k={}.csv".format(output_dir,k),'w') as f:
        wr = csv.writer(f)
        wr.writerows(randDP)

    with open("{}/syndist_k={}.csv".format(output_dir,k),'w') as f:
        wr = csv.writer(f)
        wr.writerows(synDP)
