# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:41:44 2014

@author: pablo
"""

import igraph

g = igraph.load("graph_files/output_numeric_ids.graphml")

str(g)

g.vs.attribute_names()