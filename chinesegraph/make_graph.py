import csv
import networkx as nx

words = None
with open('chinese_words.csv') as f:
    rd = csv.reader(f)
    words = [w[0] for w in rd]

chars = set()
for w in words:
    chars = chars.union(set(w))
    # Creating a little 'index'


G = nx.Graph()

for ch in chars:
    G.add_node(ch,{'chinese':ch})

for i,w in enumerate(words):
    G.add_node(str(i),{'chinese':w})
    for ch in w:
        G.add_edge(str(i),ch)

nx.write_graphml(G,'chinese_graph.graphml')
