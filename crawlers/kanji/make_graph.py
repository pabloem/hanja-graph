"""
This file keeps different functions that I've had to use to build the graph, and keep parts of it.
"""
import networkx as nx
# Takes in two dictionary objects

def make_bipartite_graph(hanjas, hanguls):
    G = nx.Graph()
    for han in hanjas:
        hanjas[han]['bipartite'] = 0
        G.add_node(han,hanjas[han])
        
    for i,han in enumerate(hanguls):
        hanguls[han]['bipartite'] = 1
        G.add_node(i+1,hanguls[han])
        edgs = [(i+1,ch) for ch in han]
        G.add_edges_from(edgs)
    return G
                


import json
import igraph
import itertools

def make_uniprojection(words,logfile = None):
    lg = set_log(logfile)
    G = igraph.Graph()
    chardic = {}
    for i,w in enumerate(words):
        w['id'] = i
        add_to_dict(w,chardic)
        G.add_vertex(w['id'])
        add_attributes(w,G.vs[w['id']])
    log(lg,"Added ids and nodes\n")

    edg_count = 0
    for i,ch in enumerate(chardic):
        nodes = chardic[ch]
        edges = list(itertools.combinations(nodes,2))
        edg_count += len(edges)
        G.add_edges(edges)
        if i+1 % 10:
            log(lg,"Added "+str(edg_count)+
                " edges for "+str(i*100.0/len(chardic))+
                "% of characters\n")
    log(lg,"Done.\n")
    return G

def log(f,line):
    if f is None: return
    f.write(line)

def set_log(logfile):
    if logfile is None:
        return None
    return open(logfile,'w')

def add_attributes(frm, to):
    for at in frm:
        to[str(at)] = frm[at]

def add_to_dict(w,chardic):
    for ch in w['chinese']:
        if ch not in chardic:
            chardic[ch] = []
        chardic[ch].append(w['id'])
            

#f = open('data/words_save_080552015.json','r')
#han_lst = json.loads(f.read())
#G = make_uniprojection(han_lst)
#G.write_graphml("hangul_uniprojection.graphml")


import json
import networkx as nx

def get_basic_nodes(basic_hanjas,G):
    b_nodes = []
    transition = set()
    for hanja in basic_hanjas:
        if hanja not in G.nodes():
            continue
        nbrs = set(G.neighbors(hanja))
        new_bn = transition & nbrs
        transition = transition - new_bn
        transition = transition | (nbrs - new_bn)
        b_nodes += list(new_bn)
    return b_nodes+basic_hanjas
