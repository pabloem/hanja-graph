import networkx as nx
import networkx.algorithms as nxa
import heapq
import number_of_walks as now
import numpy as np

class Featurator(object):
    def __init__(self,G):
        self._graph = G
        self._features = {}
        self.configure_features()

    def calculate_feature(self,feature,h1,h2):
        if feature in self._features:
            return None
        if h1 not in self._graph.nodes() or h2 not in self._graph.nodes():
            return None
        return self._features[feature](h1,h2)

    def configure_features(self):
        self._features['self_neighbor_degree_ratio'] = self.self_neighbor_degree_ratio
        self._features['two_step_walks'] = self.two_step_walk_similarity
        self._features['connected'] = self.connected


# Here goes the list of features!
    # This function returns the normalized distance in the ordered list
    # of self-neighbor degree ratios. Smaller numbers mean that both nodes
    # have a similar degree ratio compared to the
    def self_neighbor_degree_ratio(h1,h2):
        if not hasattr(self,'_deg_ratio_distances'):
            self.calculate_sn_degree_ratio()

        if h1 not in self._deg_ratio_distances:
            return self._deg_ratio_distances[h2][h1]
        return self._deg_ratio_distances[h1][h2]

    # This function returns the normalized two-step-walk similarity, calculated as follows:
    # let num_walks = number of 2-step walks between hanja A and B
    # let min_degree = minimum between degree of node A and node B
    # let normalized_num_of_walks = num_walks / min_degree
    def two_step_walk_similarity(self,h1,h2):
        if not hasattr(self,'_num_two_step_walks'):
            self.calculate_two_step_walks()
        if h1 not in self._num_two_step_walks or h2 not in self._num_two_step_walks:
            return None
        return self._num_two_step_walks[h1][h2]

    # This function returns 1 if the nodes share an edge, and 0 otherwise
    def connected(self,h1,h2):
        G = self._graph
        neighbors = G.neighbors(h1)
        return 1 if h2 in neighbors else 0

# Here goes the list of helper functions
    def calculate_two_step_walks(self):
        two_st_walks = now.all_pairs_number_of_walks(self._graph,2)
        G = self._graph

        for h1 in two_st_walks:
            for h2 in two_st_walks[h1]:
                two_st_walks[h1][h2] = (two_st_walks[h1][h2] + 0.0)/min(G.degree(h1),G.degree(h2))

        # This structure stores the NORMALIZED number of 2 step walks
        self._num_two_step_walks = two_st_walks

    def calculate_sn_degree_ratio(self):
        pq = []
        G = self._graph
        for node in G.nodes():
            deg = G.degree(node)
            if deg == 0: continue
            neighbors = G.neighbors(node)
            tot = 0.0
            for ng in neighbors:
                tot = += G.degree(ng)
            ng_avg = tot/len(neighbors)
            ratio = deg/ng_avg
            heapq.heappush(pq,(ratio,node))

        ordered = heapq.nlargest(len(pq),pq)
        positions = {}
        for i, elm in enumerate(ordered):
            positions[elm[1]] = i

        # The following array contains NORMALIZED distances
        distances = {}
        for n1 in G.nodes():
            if n1 not in positions: continue
            distances[n1] = {}
            for n2 in G.nodes():
                if n2 in distances: continue
                if n2 not in positions: continue
                distances[n1][n2] = (abs(positions[n1] - positions[n2])+0.0) / len(pq)

        self._deg_ratio_distances = distances
        return
