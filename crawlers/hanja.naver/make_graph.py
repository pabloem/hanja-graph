import networkx as nx
# Takes in two dictionary objects
class NaverGraphMaker(object):
    def __init__(this):
        pass

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
                
