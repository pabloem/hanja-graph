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

similar_pairs = [
    ['同','一'], #Dong - same, Il - one
    ['兩','二'], #Yang - both, I - two
    ['共','同'], #Gong - together, Dong - same
    ['側','面'], #Cheuk - side, Myeon - surface, plane, side
    ['法','則'], #Beob - Law, Chik - Rule
    ['職','線'], #Jik - straight, Seon - line
    ['父','母'] #Bu - father, Mo - mother
    # Shik - formula, Gyu - regulation
    # Hyeong - shape, Mo - standard, model
    # Chong - General, all, whole
]
