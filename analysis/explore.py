# encoding: utf-8
import networkx as nx
import networkx.algorithms as nxa
import json

G = nx.read_graphml('hanja_unip_2hanwds_03062015.graphml',unicode)

# The 2-hanja graph projection is not connected, thus we must get the largest
# connected component of the graph.
gen = nxa.connected_components(G)
mainLst = gen.next()
G = G.subgraph(mainLst)

if not nxa.is_connected(G) == True:
    print("We have a PROBLEM, Houston.")

lengths = nxa.all_pairs_shortest_path_length(G)
json.dump(lengths,open('splen.json','wb'))

similar_pairs =[
    [u'同',u'一'], #Dong - same, Il - one
    [u'兩',u'二'], #Yang - both, I - two
    [u'共',u'同'], #Gong - together, Dong - same
    [u'側',u'面'], #Cheuk - side, Myeon - surface, plane, side
    [u'法',u'則'], #Beob - Law, Chik - Rule
    [u'職',u'線'], #Jik - straight, Seon - line
    [u'父',u'母'] #Bu - father, Mo - mother
    # Shik - formula, Gyu - regulation
    # Hyeong - shape, Mo - standard, model
    # Chong - General, all, whole
]
