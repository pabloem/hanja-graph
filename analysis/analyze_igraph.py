# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:41:44 2014

@author: pablo
"""
import igraph

def load_in_graph(directory = "../graph_files/", filename = "graph.graphml",
                  no_unicode = False):
    """
    Load in a graph file using the igraph load function.

    Arguments:
    no_unicode -- Indicates whether or not to do a unicode transofrmation
    of the input graph.
    """
    g = igraph.load(directory+filename)

    if no_unicode:
        return g
    # We need to convert all attributes to unicode
    attribs = ['chinese','label','korean','meaning']
    for elm in g.vs:
        for atr in attribs:
            try:
                elm[atr] = unicode(elm[atr],'utf-8')
            except KeyError:
                pass
    return g

g = load_in_graph()
bp = g.bipartite_projection()
hanja_graph = bp[0]
korean_graph = bp[1]

def recalculate_weights(kor_gr,han_gr):
    """
    Recalculate edge weights of Korean uniprojection of the bipartite graph.
    This method is not working ATM
    """
    # We add a structure to address the hanja graph directly
    dirct_han = dict() 
    for i,elm in enumerate(han_gr.vs):
        dirct_han[elm['chinese']] = i

    for elm in kor_gr.es:
        src = kor_gr.vs[elm.source]
        trg = kor_gr.vs[elm.target]
        diffs = list()
        for char in src['chinese']+trg['chinese']:
            if (char not in src['chinese'] or 
                char not in trg['chinese']):
                diffs.append(char)
        if len(diffs) == 0:
            elm['weight'] = 0.0
            continue

        import itertools
        edge_ids = [han_gr.get_eid(dirct_han[A[0]],dirct_han[A[1]]) for A in itertools.combinations(diffs,2)]
        edge_weights = sum([han_gr.es[eid]['weight'] for eid in edge_ids])
        elm['weight'] = edge_weights
    pass
