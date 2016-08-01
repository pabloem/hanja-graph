import requests as r
import csv
import json
import urllib.parse as up
from bs4 import BeautifulSoup
import time

G = nx.read_graphml('chinese_graph.graphml')

wds = list(G.node[a]['chinese'] for a in G.node.keys() if 'word' in G.node[a])

baseUrl = "http://www.chinesetools.eu/tools/synonym/"
baseUrl = "http://www.iciba.com/%20"
#?q=%26%2323453%3B%26%2336149%3B&Submit=Search
synPairs = []
antPairs = []

for i,w in enumerate(wds):
    if i % 20 == 0: 
        print("Done {} words. Got {} synonyms, {} antonyms."
              .format(i,len(synPairs),len(antPairs)))
    time.sleep(0.2)
    res = r.get(baseUrl+w)
    sp = BeautifulSoup(res.text)
    ows = sp.select('.opposite-word')
    if len(ows) == 0: continue
    art = ows[0].parent
    dvs = art.select('div')
    doneSyn = False
    for dv in dvs[1:]: # Skipping the first one...
        if dv['class'] == 'opposite-word':
            doneSyn = True
            continue
        txt = dv.select('a')[0].text.strip()
        if not doneSyn: 
            synPairs.append([w,txt])
        else: 
            antPairs.append([w,txt])
    

with open('chineseSyn.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(synPairs)

with open('chineseAnt.csv','w') as f:
    wr = csv.writer(f)
    wr.writerows(antPairs)
