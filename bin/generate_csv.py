#!/usr/bin/python3
from analysis.Featurator import Featurator
import networkx as nx
import networkx.algorithms as nxa
import csv
import sys

if len(sys.argv) < 3:
    print("Usage: ./generate_csv.py graph_file output_file [#processes]")
    sys.exit()

graph_file = sys.argv[1]
output_file = sys.argv[2]
processes = 1 if len(sys.argv) < 4 else int(sys.argv[3])

print("Loading graph file...")
G = nx.read_graphml(graph_file)

print("Obtaining largest connected component...")
gen = nxa.connected_components(G)
mainLst = next(gen)
G = G.subgraph(mainLst)

f = Featurator(G)

csv_fields = ['pair','h1','h2'] + f.feature_list()

csvfile =  open(output_file,'w')
writer = csv.DictWriter(csvfile,fieldnames=csv_fields)
writer.writeheader()

count = 0

pairs = [(h1, h2) for i,h1 in enumerate(G.nodes()) for j,h2 in enumerate(G.nodes()) if j > i]

print("Starting...")
for pair in pairs:
    h1 = pair[0]
    h2 = pair[1]
    count += 1
    if count % 1000 == 0: print("Done "+str(count)+" pairs")
    #res = f.get_feature_dict(h1,h2)
    res = dict()
    res['pair'] = h1+h2 if h1 < h2 else h2+h1
    res['h1'] = h1 if h1 < h2 else h2
    res['h2'] = h2 if h1 < h2 else h1
    #writer.writerow(res)

csvfile.close()
