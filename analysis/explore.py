# encoding: utf-8
import networkx as nx
import networkx.algorithms as nxa
import json
import os.path

G = nx.read_graphml('hanja_unip_2hanwds_03062015.graphml',unicode)

# The 2-hanja graph projection is not connected, thus we must get the largest
# connected component of the graph.
gen = nxa.connected_components(G)
mainLst = gen.next()
G = G.subgraph(mainLst)

if nxa.is_connected(G) == False:
    print("We have a PROBLEM, Houston.")
    return

lengths = 0
if not os.path.isfile('splen.json'):
    lengths = nxa.all_pairs_shortest_path_length(G)
    json.dump(lengths,open('splen.json','wb'))
else:
    with open('splen.json') as data_file:
        lengths = json.load(data_file)


sp_distances = {}
distance_count = {}
if not os.path.isfile('distcount.json'):
    for h1 in lengths:
        for h2 in lengths[h1]:
            if lengths[h1][h2] not in distance_count:
                distance_count[lengths[h1][h2]] = 0
                distance_count[lengths[h1][h2]] += 1

    # We divide by 2, because we double-counted every pair
    for num in distance_count:
        distance_count[num] = distance_count[num]/2

    similar_pairs =[
        [u'同',u'一'], #Dong - same, Il - one
        [u'兩',u'二'], #Yang - both, I - two
        [u'共',u'同'], #Gong - together, Dong - same
        [u'側',u'面'], #Cheuk - side, Myeon - surface, plane, side
        [u'法',u'則'], #Beob - Law, Chik - Rule
        [u'職',u'線'], #Jik - straight, Seon - line
        [u'父',u'母'], #Bu - father, Mo - mother
        [u'業',u'職'], #Eob - business trade, Jik - duty, profession
        [u'人',u'者']  #In - person, Ja - That, who, he
        [u'回',u'環'] # Hoe - return, turn around, Hwan - ring, bracelet
        [u'見',u'視'] # Kyeon - Observe, percieve, Shi - Inspect, observe, see
        [u'聞',u'聽'] # Moon - Hear, make known, Cheong - Hear, listen
        # Shik - formula, Gyu - regulation
        # Hyeong - shape, Mo - standard, model
        # Chong - General, all, whole
    ]

    for lst in similar_pairs:
        h1 = lst[0]
        h2 = lst[1]
        if lengths[h1][h2] not in sp_distances:
            sp_distances[lengths[h1][h2]] = 0
            sp_distances[lengths[h1][h2]] += 1

    del lengths

    json.dump({'all_nodes': distance_count, 
               'similar_pairs': sp_distances},
              open('distcount.json','wb'))
else:
    with open('distcount.json') as data_file:
        distances = json.load(data_file)
        sp_distances = distances['similar_pairs']
        distance_count = distances['all_nodes']
        
avg_distance = nxa.average_shortest_path_length(G)
