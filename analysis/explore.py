# encoding: utf-8
import networkx as nx
import networkx.algorithms as nxa
import json
import os.path

G = nx.read_graphml('hanja_unip_2hanwds_03062015.graphml',unicode)


similar_pairs =[
    [u'同',u'一'], #Dong - same, Il - one
    [u'兩',u'二'], #Yang - both, I - two
    [u'共',u'同'], #Gong - together, Dong - same
    [u'側',u'面'], #Cheuk - side, Myeon - surface, plane, side
    [u'法',u'則'], #Beob - Law, Chik - Rule
    [u'職',u'線'], #Jik - straight, Seon - line
    [u'父',u'母'], #Bu - father, Mo - mother
    [u'業',u'職'], #Eob - business trade, Jik - duty, profession
    [u'人',u'者'],  #In - person, Ja - That, who, he
    [u'回',u'環'], # Hoe - return, turn around, Hwan - ring, bracelet
    [u'見',u'視'], # Kyeon - Observe, percieve, Shi - Inspect, observe, see
    [u'聞',u'聽'] # Moon - Hear, make known, Cheong - Hear, listen
    # [u'事',     #Sa - Affair, business
    # [u'今',     # Geum - now, today
    # Extra: 冷-Neng,cold | 溫-On,warm | 0.170588235294
    # Shik - formula, Gyu - regulation
    # Hyeong - shape, Mo - standard, model
    # Chong - General, all, whole
]

# The 2-hanja graph projection is not connected, thus we must get the largest
# connected component of the graph.
gen = nxa.connected_components(G)
mainLst = gen.next()
G = G.subgraph(mainLst)

if nxa.is_connected(G) == False:
    print("We have a PROBLEM, Houston.")

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

import number_of_walks as now
import numpy as np

num_2step_walks = now.all_pairs_number_of_walks(G,2)

num_2step_walk_dist = {}
normalized_2step_w = []
for h1 in num_2step_walks:
    for h2 in num_2step_walks[h1]:
        if h1 == h2: continue
        if num_2step_walks[h1][h2] not in num_2step_walk_dist:
            num_2step_walk_dist[num_2step_walks[h1][h2]] = 0
        num_2step_walk_dist[num_2step_walks[h1][h2]] += 1
        if num_2step_walks[h1][h2] == 0: continue
        normalized_2step_w.append(num_2step_walks[h1][h2]/(min(G.degree(h1),G.degree(h2))+.0))


sp_normalized_nw = []
sp_num_walks = {}
for lst in similar_pairs:
    h1 = lst[0]
    h2 = lst[1]
    if num_2step_walks[h1][h2] not in sp_num_walks:
        sp_num_walks[num_2step_walks[h1][h2]] = 0
    sp_num_walks[num_2step_walks[h1][h2]] += 1
    if num_2step_walks[h1][h2] == 0: continue
    sp_normalized_nw.append(num_2step_walks[h1][h2]/(min(G.degree(h1),G.degree(h2))+.0))

# We divide by 2, because we double-counted every pair
for elm in sp_num_walks:
    sp_num_walks[elm] = sp_num_walks[elm]/2

gen_99pc = np.percentile(normalized_2step_w,99)
gen_95pc = np.percentile(normalized_2step_w,95)
deg_50pc = np.mean(G.degree().values())
deg_99pc = np.percentile(G.degree().values(),99)
del normalized_2step_w


print("The following is the list of characters scoring high on similarity.")
firsts = set()
for h1 in num_2step_walks:
    firsts.add(h1)
    for h2 in num_2step_walks[h1]:
        if h1 == h2: continue
        if h2 in firsts: continue
        if G.degree(h1) == 0 or G.degree(h2) == 0: continue
        norm_2sp_wks = num_2step_walks[h1][h2]/(min(G.degree(h1),G.degree(h2))+.0)
        if norm_2sp_wks >= gen_95pc and min(G.degree(h1),G.degree(h2)) >= deg_50pc:
            h1Eng = '' if 'english' not in G.node[h1] else G.node[h1]['english']
            h2Eng = '' if 'english' not in G.node[h2] else G.node[h2]['english']
            print(h1+"("+G.node[h1]['pronunciation']+") - "+ h1Eng+" | "+h2+"("+G.node[h2]['pronunciation']+") - "+ h2Eng+" | "+str(norm_2sp_wks))
del firsts
