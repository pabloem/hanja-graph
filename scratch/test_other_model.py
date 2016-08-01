import csv
import networkx as nx
import numpy as np
from random import choice

#G = nx.read_graphml('graphs/chinese_graph.graphml')
#gen = nx.connected_component_subgraphs(G)
#G = next(gen)

#sts = nx.bipartite.sets(G)

#words = None
#hanjas = None
#wordSet = None
#if len(sts[0]) > 6000: 
#    words = list(sts[0])
#    wordSet = sts[0]
#    hanjas = list(sts[1])
#else: 
#    words = list(sts[1])
#    wordSet = sts[1]
#    hanjas = list(sts[0])

#wordic = {G.node[e]['chinese']:k for k,e in enumerate(words)}

_lst = None
with open('scratch/mono_trained_Zh_vectors.txt') as f:
    _lst = list(f)

ks = None
with open('chinesegraph/all_chinese_synonyms.csv') as f:
    rd = csv.reader(f)
    ks = list(rd)
    synSet = set(a for pr in ks for a in pr)

stanfordWords = []
stanfordVectors = []
stanfordIndex = {}
ignored = 0
for ln in _lst:
    sp = ln.split(" ")
    wd = sp[0].strip()
    vec = sp[1].strip()
    if wd not in synSet: 
        ignored += 1
        continue
    stanfordIndex[wd] = len(stanfordWords)
    stanfordWords.append(wd)
    stanfordVectors.append([float(a) for a in vec.split(",")])
    

synDp = []
ranDp = []
for s in ks:
    if s[0] not in stanfordIndex or s[1] not in stanfordIndex: continue
    v1 = np.asarray(stanfordVectors[stanfordIndex[s[0]]])
    v2 = np.asarray(stanfordVectors[stanfordIndex[s[1]]])
    synDp.append(np.dot(v1,v2))
    
for s in ks:
    if s[0] not in stanfordIndex and s[1] not in stanfordIndex: continue
    v1 = np.asarray(choice(stanfordVectors))
    v2 = np.asarray(choice(stanfordVectors))
    ranDp.append(np.dot(v1,v2))

"""
with open('stanford_dotsyn.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows([[a] for a in synDp])

with open('stanford_dotran.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows([[a] for a in ranDp])
"""

import matplotlib.pyplot as plt
import seaborn as sns
from statistics import stdev

sd = stdev(ranDp)
sns.set(color_codes=True)
sns.set(style="white", palette="muted")
 
ax = sns.distplot(ranDp,hist=True,kde=False,label="Random pairs")
ax = sns.distplot(synDp,hist=True,kde=False,label="Synonym pairs")
ax.set_yscale('log')
ax.grid(True)
ax.set_xlabel("Inner product between vectors")
ax.set_ylabel("Frequency")
ax.legend()
ax.axvline(sd,label="random data stdev")
ax.axvline(-sd)

ranProp = sum(1.0 if abs(rd) > sd else 0.0 for rd in ranDp)/len(ranDp)
synProp = sum(1.0 if abs(rd) > sd else 0.0 for rd in synDp)/len(synDp)
print("Ran classification. Misclassified random pairs: {}. Accurately classified synonyms: {}"
          .format(ranProp,synProp))

ax.annotate("Synonyms outside stdev (random): {:.4f}".format(synProp),xy=(0.1,0.8),xycoords='axes fraction')
ax.annotate("Random pairs outside stdev (random): {:.4f}".format(ranProp),xy=(0.1,0.75),xycoords='axes fraction')

plt.suptitle("Dot product between random pairs of word and pairs of synonyms")

plt.savefig("other_hist.png")
plt.show()
