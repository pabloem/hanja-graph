# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 16:42:31 2014

@author: pablo
"""

from lxml import etree

def make_gexf_tree(words,hanjas,links):
    
    root = etree.Element("gexf",version="1.2")

    root.append(\
        etree.Element("graph", \
            mode="static",\
            defaultedgetype="undirected"\
            )\
        )

    graph_node = root[0]
    
    graph_node.append(etree.Element("nodes"))
    graph_node.append(etree.Element("edges"))
    
    nodes = graph_node[0]
    edges = graph_node[1]
    
    for word in words:
        nodes.append(etree.Element("node",word))
    
    for hanja in hanjas:
        nodes.append(etree.Element("node",hanja))
    
    for link in links:
        edges.append(etree.Element("edge",\
                        source=link['source'],\
                        target=link['target'],\
                        id=str(link['id'])\
                    ))
        
    return root