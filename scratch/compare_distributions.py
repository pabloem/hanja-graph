import networkx as nx
import numpy as np
import scipy as sp
import csv
import time
from random import choice
from math import log

G = nx.read_graphml('graphs/bipartite_graph.graphml') # Korean language graph
#G = nx.read_graphml('graphs/chinese_graph.graphml') # Chinese graph

gen = nx.connected_component_subgraphs(G)
G = next(gen)
output_dir = "tmpDistancesFull2"

sts = nx.bipartite.sets(G)

words = None
hanjas = None
wordSet = None
if len(sts[0]) > 6000: 
    words = list(sts[0])
    wordSet = sts[0]
    hanjas = list(sts[1])
else: 
    words = list(sts[1])
    wordSet = sts[1]
    hanjas = list(sts[0])

wordic = {G.node[e]['chinese']:k for k,e in enumerate(words)}

synonyms = None
with open('scratch/korean_synonyms.csv') as f:
#with open('chinesegraph/chinese_synonyms.csv') as f:
    rd = csv.reader(f)
    synonyms = list(rd)

synDP = []
randDP = []

A = nx.bipartite.biadjacency_matrix(G,hanjas)
#A = A.asfptype()
#A = A.tolil()
A = A.astype(float)

weight = True # In case we want to do TF-IDF weighting
weight = False # In case we chose not to do TF-IDF weighting
if weight:
    rowsums = A.sum(axis=1)
    colsums = A.sum(axis=0)
    print("Starting matrix weighting...")
    for rn in range(A.shape[0]): # Row num
        for cn in range(A.shape[1]):
            if A[rn,cn] == 0: continue
            A[rn,cn] = A[rn,cn]/colsums[0,cn] * log(A.shape[1]/rowsums[rn,0])
    print("Done weighting the matrix.")

minK = 666
maxK = 668
print("Starting")
for k in range(minK,maxK,200):
    st = time.clock()
    print("Factorizing for k={}".format(k))
    U,s,V = sp.sparse.linalg.svds(A,k)
    Vtr = V.transpose()
    #Vtr = A.transpose()
    break

    print("Factorized. Obtaining distribution.")
    for pr in synonyms:
        c1 = pr[0]
        c2 = pr[1]
        if c1 not in wordic or c2 not in wordic: continue
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
    print("Saving. Took {} seconds for k={}. Worked with {} syn, {} random pairs."
          .format(end-st,k,len(synDP),len(randDP)))
    with open("{}/randdist_k={}.csv".format(output_dir,k),'w') as f:
        wr = csv.writer(f)
        wr.writerows([[r] for r in randDP])

    with open("{}/syndist_k={}.csv".format(output_dir,k),'w') as f:
        wr = csv.writer(f)
        wr.writerows(synDP)
