# encoding: utf-8
import networkx as nx
import networkx.algorithms as nxa

G = nx.read_graphml('hanja_unip.graphml',unicode)


# The 2-hanja graph projection is not connected, thus we must get the largest
# connected component of the graph.
gen = nxa.connected_components(G)
mainLst = gen.next()
G = G.subgraph(mainLst)

if nxa.is_connected(G) == False:
    print("We have a PROBLEM, Houston.")

        
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
        normalized_2step_w.append(num_2step_walks[h1][h2]/((G.degree(h1)*G.degree(h2))+.0))

gen_99pc = np.percentile(normalized_2step_w,99)
gen_98pc = np.percentile(normalized_2step_w,98)
gen_97pc = np.percentile(normalized_2step_w,97)
gen_96pc = np.percentile(normalized_2step_w,96)
gen_95pc = np.percentile(normalized_2step_w,95)
del normalized_2step_w
deg_50pc = np.percentile(G.degree().values(),50)
deg_99pc = np.percentile(G.degree().values(),99)


print("The following is the list of characters scoring high on similarity.")
firsts = set()
for h1 in num_2step_walks:
    firsts.add(h1)
    for h2 in num_2step_walks[h1]:
        if h1 == h2: continue
        if h2 in firsts: continue
        if G.degree(h1) == 0 or G.degree(h2) == 0: continue
        if G.degree(h1)*3 < G.degree(h2) or G.degree(h2)*3 < G.degree(h1): continue
        norm_2sp_wks = num_2step_walks[h1][h2]/((G.degree(h1)*G.degree(h2))+.0)
        if norm_2sp_wks >= gen_98pc and min(G.degree(h1),G.degree(h2)) >= deg_50pc:
            h1Eng = '' if 'english' not in G.node[h1] else G.node[h1]['english']
            h2Eng = '' if 'english' not in G.node[h2] else G.node[h2]['english']
            print(h1+"("+G.node[h1]['pronunciation']+") - "+ h1Eng+" | "+h2+"("+G.node[h2]['pronunciation']+") - "+ h2Eng+" | "+str(norm_2sp_wks)
                  +" | Degrees: "+str(G.degree(h1))+", "+str(G.degree(h2)))
del firsts
