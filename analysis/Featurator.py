import networkx as nx
import networkx.algorithms as nxa
import heapq
import sys
import numpy as np

print(sys.path)
import number_of_walks as now


class Featurator(object):
    def __init__(self,G,radicals=None):
        self._graph = G
        self._got_rads = False
        if radicals is not None:
            self._got_rads = True
            self._rads = radicals;
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
        self._features['reciprocity'] = self.connected
        self._features['degree_difference'] = self.degree_difference
        self._features['degree_sum'] = self.degree_sum
        self._features['degree_ratio'] = self.degree_ratio  # Does this make sense?
        self._features['dispersion'] = self.dispersion
        #self._features['edge_connectivity'] = self.edge_connectivity # Note - this feature is way too slow...
        #self._features['node_connectivity'] = self.node_connectivity # Note - this feature is way too slow...
        self._features['clustering_difference'] = self.clustering_difference
        self._features['clustering_sum'] = self.clustering_sum
        self._features['clustering_rate'] = self.clustering_rate
        self._features['closeness_difference'] = self.closeness_difference
        self._features['closeness_sum'] = self.closeness_sum
        self._features['betweenness_difference'] = self.betweenness_difference
        self._features['betweenness_sum'] = self.betweenness_sum
        self._features['pagerank_difference'] = self.pagerank_difference
        self._features['pagerank_sum'] = self.pagerank_sum
        self._features['shortest_distance'] = self.shortest_path_length
        self._features['same_7_clique_com'] = self.same_7_clique_com
        self._features['same_6_clique_com'] = self.same_6_clique_com
        if self._got_rads:
            self._features['share_radical'] = self.share_radical
            self._features['shared_radicals'] = self.shared_radicals


    def share_radical(self,h1,h2):
        sh1 = set(self._rads[h1])
        sh2 = set(self._rads[h2])
        return 1 if len(sh1.intersection(sh2)) > 0 else 0

    def shared_radicals(self,h1,h2):
        return (len(set(self._rads[h1]).intersection(set(self._rads[h2])))/max(len(self._rads[h1])+0.0,len(self._rads[h2])+0.0,1.0))
            
    def feature_list(self):
        return list(self._features.keys())

    def get_feature_dict(self,h1,h2):
        res = {}
        for feature in self.feature_list():
            res[feature] = self._features[feature](h1,h2)
        return res


# Here goes the list of features!
    # This function returns the normalized distance in the ordered list
    # of self-neighbor degree ratios. Smaller numbers mean that both nodes
    # have a similar degree ratio compared to the
    def self_neighbor_degree_ratio(self,h1,h2):
        if not hasattr(self,'_deg_ratio_distances'):
            self.calculate_sn_degree_ratio()

        if h1 not in self._deg_ratio_distances:
            return self._deg_ratio_distances[h2][h1]
        return self._deg_ratio_distances[h1][h2]

    def same_7_clique_com(self,h1,h2):
        if not hasattr(self,'_7_clique_coms'):
            self._get_7_clique_coms()

        for comset in self._7_clique_coms:
            if h1 in comset and h2 in comset: return 1
        return 0

    def same_6_clique_com(self,h1,h2):
        if not hasattr(self,'_6_clique_coms'):
            self._get_6_clique_coms()
        for comset in self._6_clique_coms:
            if h1 in comset and h2 in comset: return 1
        return 0

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

    # This function returns the absolute difference between the degree of both nodes
    def degree_difference(self,h1,h2):
        G = self._graph
        return abs(G.degree(h1) - G.degree(h2))

    # This function returns the absolute difference between the degree of both nodes
    def degree_sum(self,h1,h2):
        G = self._graph
        return G.degree(h1) + G.degree(h2)

    # This function returns the ratio of min_degree(A,B) divided by max_degree(A,B)
    def degree_ratio(self,h1,h2):
        G = self._graph
        deg_ratio = (G.degree(h1)+0.0)/G.degree(h2)
        return deg_ratio if deg_ratio <= 1 else 1/deg_ratio

    # This function returns normalized dispersion
    # See: Romantic Partnerships and the Dispersion of Social Ties: 
    #      A Network Analysis of Relationship Status on Facebook. 
    #      Lars Backstrom, Jon Kleinberg.
    def dispersion(self,h1,h2):
        G = self._graph
        return nxa.dispersion(G,h1,h2,True)

    # This function returns the minimum number of edges to remove to disconnect
    # nodes h1 and h2.
    def edge_connectivity(self,h1,h2):
        G = self._graph
        return nxa.edge_connectivity(G,h1,h2)

    # This function returns the minimum number of nodes to remove to disconnect
    # nodes h1 and h2
    def node_connectivity(self,h1,h2):
        G = self._graph
        return nxa.node_connectivity(G,h1,h2)

    # This function returns the absolute difference between the clustering 
    # coefficient of both nodes
    def clustering_difference(self,h1,h2):
        G = self._graph
        c_h1 = nxa.clustering(G,h1)
        c_h2 = nxa.clustering(G,h2)
        return abs(c_h1 - c_h2)

    # This function returns the sum of the clustering 
    # coefficient of both nodes
    def clustering_sum(self,h1,h2):
        G = self._graph
        c_h1 = nxa.clustering(G,h1)
        c_h2 = nxa.clustering(G,h2)
        return c_h1 + c_h2

    # This function returns the absolute difference between the clustering 
    # coefficient of both nodes
    def clustering_rate(self,h1,h2):
        G = self._graph
        c_h1 = nxa.clustering(G,h1)
        c_h2 = nxa.clustering(G,h2)
        min_degree = min(max(1,G.degree(h1)),max(1,G.degree(h2)))+0.0
        return c_h1*c_h2/min_degree

    # This function returns the absolute difference between the closeness centrality
    # of both nodes
    def closeness_difference(self,h1,h2):
        G = self._graph
        c_h1 = nxa.closeness_centrality(G,h1)
        c_h2 = nxa.closeness_centrality(G,h2)
        return abs(c_h1 - c_h2)

    # This function returns the sum of the closeness centrality
    # of both nodes
    def closeness_sum(self,h1,h2):
        G = self._graph
        c_h1 = nxa.closeness_centrality(G,h1)
        c_h2 = nxa.closeness_centrality(G,h2)
        return c_h1 + c_h2

    # This function returns the absolute difference between the betweenness centrality
    # of both nodes
    def betweenness_difference(self,h1,h2):
        if not hasattr(self,'_betweenness_centralities'):
            self.calculate_betweenness_centrality()
        return abs(self._betweenness_centralities[h1] - self._betweenness_centralities[h2])

    # This function returns the absolute difference between the betweenness centrality
    # of both nodes
    def betweenness_sum(self,h1,h2):
        if not hasattr(self,'_betweenness_centralities'):
            self.calculate_betweenness_centrality()
        return self._betweenness_centralities[h1] + self._betweenness_centralities[h2]

    # This function returns the absolute difference between the pagerank centrality
    # of both nodes
    def pagerank_difference(self,h1,h2):
        if not hasattr(self,'_pageranks'):
            self.calculate_pagerank()
        return abs(self._pageranks[h1] - self._pageranks[h2])

    # This function returns the sum of the pagerank centrality
    # of both nodes
    def pagerank_sum(self,h1,h2):
        if not hasattr(self,'_pageranks'):
            self.calculate_pagerank()
        return self._pageranks[h1] + self._pageranks[h2]

    # This function returns the shortest path length between both nodes, or 0 if they are not connected
    def shortest_path_length(self,h1,h2):
        G = self._graph
        try:
            return nxa.shortest_path_length(G,h1,h2)
        except NetworkXNoPath:
            return 0

# Here goes the list of helper functions

    def _get_7_clique_coms(self):
        G = self._graph
        coms = nxa.k_clique_communities(G,7)
        self._7_clique_coms = []
        for com in coms:
            self._7_clique_coms.append(com)

    def _get_6_clique_coms(self):
        G = self._graph
        coms = nxa.k_clique_communities(G,6)
        self._6_clique_coms = []
        for com in coms:
            self._6_clique_coms.append(com)

        
    def calculate_two_step_walks(self):
        two_st_walks = now.all_pairs_number_of_walks(self._graph,2)
        G = self._graph

        for h1 in two_st_walks:
            for h2 in two_st_walks[h1]:
                if G.degree(h1) == 0 or G.degree(h2) == 0:
                    two_st_walks[h1][h2] = 0
                    continue
                two_st_walks[h1][h2] = (two_st_walks[h1][h2] + 0.0)/min(G.degree(h1),G.degree(h2))

        # This structure stores the NORMALIZED number of 2 step walks
        self._num_two_step_walks = two_st_walks

    def calculate_pagerank(self):
        G = self._graph
        pr = nx.pagerank_scipy(G)
        self._pageranks = pr

    def calculate_betweenness_centrality(self):
        G = self._graph
        self._betweenness_centralities = nxa.betweenness_centrality(G)

    def calculate_sn_degree_ratio(self):
        pq = []
        G = self._graph
        for node in G.nodes():
            deg = G.degree(node)
            if deg == 0: continue
            neighbors = G.neighbors(node)
            tot = 0.0
            for ng in neighbors:
                tot += G.degree(ng)
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
