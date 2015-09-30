#!/usr/bin/python
import sys
import json
import networkx as nx

exp = """
Usage: ./make_kanji_graph.py input_json output_graphml
- The input_json is a file with a JSON dictionary having a special formatting. The dictionary has three fields:
  - 'kanji' - Is a list of Kanjis. They contain their 'chinese', 'english', 'kunyomi', and 'onyomi' fields.
  - 'words' - Is a list of Japanese words. They contain 'chinese', 'english', and 'japanese' fields.
"""
if len(sys.argv) < 3:
    print(exp)
    sys.exit(0)

in_file = sys.argv[1]
out_file = sys.argv[2]

f = open(in_file)
d = json.load(f)

kanjis = d['kanji']
words = d['words']

print("Kanji: "+str(len(kanjis))+" | Words: "+str(len(words)))

G = nx.Graph()
nodes = 0
edges = 0
for k in kanjis:
    k['bipartite'] = 0
    G.add_node(k['chinese'],k)
    nodes += 1

for i,w in enumerate(words):
    w['bipartite'] = 1
    G.add_node(i+1,w)
    nodes += 1
    for ch in w['chinese']:
        if ch in G.node:
            G.add_edge(i+1,ch)
            edges += 1

print("Nodes: "+str(nodes)+" | Edges: "+str(edges))

nx.write_graphml(G,out_file)
