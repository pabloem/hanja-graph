# encoding: utf-8
import networkx as nx
import networkx.algorithms as nxa
import heapq
import io
import json

G = nx.read_graphml('hanja_unip.graphml',unicode)


# The 2-hanja graph projection is not connected, thus we must get the largest
# connected component of the graph.
gen = nxa.connected_components(G)
mainLst = gen.next()
G = G.subgraph(mainLst)

if nxa.is_connected(G) == False:
    print("We have a PROBLEM, Houston.")

priQ = []
for node in G.nodes():
    deg = G.degree(node)
    if deg == 0: continue
    neighbors = G.neighbors(node)
    tot = 0.0
    for ng in neighbors:
        tot += G.degree(ng)
    ng_avg = tot/len(neighbors)
    ratio = deg/ng_avg
    heapq.heappush(priQ,(ratio,str(G.node[node]),G.node[node]['chinese']))

ordered = heapq.nlargest(len(priQ),priQ)

with io.open('ratios.json','w',encoding='utf8') as json_file:
    json.dump(ordered,json_file, ensure_ascii=False,sort_keys=True,indent=4, separators=(',', ': '))

positions = dict()
for i,elm in enumerate(ordered):
    positions[elm[2]] = i

distances = dict()
for n1 in G.nodes():
    if n1 not in positions: continue
    distances[n1] = dict()
    for n2 in G.nodes():
        if n2 in distances: continue
        if n2 not in positions: continue
        distances[n1][n2] = abs(positions[n1] - positions[n2])

with io.open('distances.json','w',encoding='utf8') as json_file:
    json.dump(distances,json_file, ensure_ascii=False,sort_keys=True,indent=4, separators=(',', ': '))
