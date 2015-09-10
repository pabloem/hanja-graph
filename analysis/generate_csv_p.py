#!/usr/bin/python3
from Featurator import Featurator
import networkx as nx
import networkx.algorithms as nxa
import csv
import sys
import multiprocessing as mp
from multiprocessing import Queue, Process

if len(sys.argv) < 3:
    print("Usage: ./generate_csv.py graph_file output_file [#processes]")
    sys.exit()

def calculate_features(queue,g_file, pairs):
    G = nx.read_graphml(graph_file)
    gen = nxa.connected_components(G)
    mainLst = next(gen)
    G = G.subgraph(mainLst)
    f = Featurator(G)
    print(g_file)
    print(str(len(pairs)))

    count = 0
    
    for pair in pairs:
        h1 = pair[0]
        h2 = pair[1]
        res = f.get_feature_dict(h1,h2)
        #res = dict()
        res['pair'] = h1+h2 if h1 < h2 else h2+h1
        res['h1'] = h1 if h1 < h2 else h2
        res['h2'] = h2 if h1 < h2 else h1
        # PUT PAIR IN QUEUE!
        queue.put(res)
        count += 1
        if count % 2000 == 1: print("Calculated " + str(count)+" elements")
    queue.put('done')

graph_file = sys.argv[1]
output_file = sys.argv[2]
processes = 1 if len(sys.argv) < 4 else int(sys.argv[3])

print("Graph file: "+graph_file +" | Output: "+output_file+" | Processes: "+str(processes))

print("Loading graph file...")
G = nx.read_graphml(graph_file)

print("Obtaining largest connected component...")
gen = nxa.connected_components(G)
mainLst = next(gen)
G = G.subgraph(mainLst)

pairs = [(h1, h2) for i,h1 in enumerate(G.nodes()) for j,h2 in enumerate(G.nodes()) if j > i]

def chunks(l, n):
    for i in range(0,len(l),n):
        print("Yielding from "+str(i)+" to "+str(i+n))
        yield l[i:i+n]

pair_chunks = list(chunks(pairs,len(pairs)//processes+1))
print(str(len(pair_chunks)))

pList = []
q = Queue()
for i in range(processes):
    p = Process(target=calculate_features,args=(q,graph_file,pair_chunks[i]))
    p.start()
    pList.append(p)


f = Featurator(G)

csv_fields = ['pair','h1','h2'] + f.feature_list()

csvfile =  open(output_file,'w')
writer = csv.DictWriter(csvfile,fieldnames=csv_fields)
writer.writeheader()

done = 0
count = 0
while True:
    res = q.get()
    count += 1
    if count % 1000 == 1:
        print("Added total of " +str(count)+" pairs.")
    if res == 'done': 
        done += 1
        if done == processes: break
        continue
    writer.writerow(res)

csvfile.close()
