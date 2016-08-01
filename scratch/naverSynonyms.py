import networkx as nx
import requests as r
from bs4 import BeautifulSoup
from itertools import combinations
import csv

G = nx.read_graphml("graphs/bipartite_graph.graphml")
sts = nx.bipartite.sets(G)

wSt = list(sts[0])
words = [G.node[ndId]['chinese'] for ndId in wSt]

synLst = []
antLst = []

baseUrl = "http://hanja.naver.com/word?q="
nwI = 0
for i,wd in enumerate(words):
    if i < nwI: continue
    if i % 1000 == 0:
        print("Got {} words. Have {} antonyms and {} synonyms.".format(i+1,len(antLst),len(synLst)))
    pg = r.get(baseUrl+wd)
    sp = BeautifulSoup(pg.text)
    w_txt = sp.select(".word_txt")
    if len(w_txt) == 0: continue
    synLis = None
    antLis = None
    for wt in w_txt:
        for i,bs in enumerate(wt.select(".blue strong")):
            if bs.text == "같은 뜻을 가진 한자어": 
                synLis = wt.select("ul")[i].select("li")
            if bs.text == '반대 뜻을 가진 한자어':
                antLis = wt.select("ul")[i].select("li")

    if synLis is not None:
        wds = [li.select_one("em").text for li in synLis]
        for syn in wds:
            synLst.append([wd,syn])

    if antLis is not None:
        wds = [li.select_one("em").text for li in antLis]
        for syn in wds:
            antLst.append([wd,syn])
    pass

#synSet = set(synLst)
#synLst = list(synSet)
#with open('korean_synonyms.csv','w') as f:
#    wr = csv.writer(f)
#    wr.writerows(synLst)

synSet = set((a[0],a[1]) for a in synLst)
synLst = list(synSet)
with open('korean_synonyms2.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(synLst)

antSet = set((a[0],a[1]) for a in antLst)
antLst = list(antSet)
with open('korean_antonyms.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(antLst)
