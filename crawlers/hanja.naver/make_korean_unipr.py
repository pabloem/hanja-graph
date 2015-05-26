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
