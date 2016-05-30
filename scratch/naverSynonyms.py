import networkx as nx
import requests as r
from bs4 import BeautifulSoup
from itertools import combinations

G = nx.read_graphml("graphs/bipartite_graph.graphml")
sts = nx.bipartite.sets(G)

wSt = list(sts[0])
words = [G.node[ndId]['chinese'] for ndId in wSt]

synLst = []
otherSynLst = []

baseUrl = "http://hanja.naver.com/word?q="
for i,wd in enumerate(words):
    if i % 1000 == 0:
        print("Got {} words. Have {} combinations and {} synonyms.".format(i+1,len(synLst),len(otherSynLst)))
    pg = r.get(baseUrl+wd)
    sp = BeautifulSoup(pg.text)
    w_txt = sp.select(".word_txt")
    if len(w_txt) == 0: continue
    synWt = None
    for wt in w_txt:
        if wt.select_one(".blue strong").text == "같은 뜻을 가진 한자어": synWt = wt
    if synWt is None: continue
    lis = synWt.select("ul li")
    wds = [li.select_one("em").text for li in lis]
    if wd not in wds: wds.append(wd)
    synLst += list(combinations(wds,2))
    for syn in wds:
        otherSynLst.append([wd,syn])
    pass

with open('korean_synonyms.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(synLst)

with open('korean_synonyms2.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(otherSynLst)

