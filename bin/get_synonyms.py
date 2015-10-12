#!/usr/bin/python
# Usage: ./get_synonyms.py input_csv training_csv output
import csv
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

rfc = RandomForestClassifier()
#rfc = SVC(gamma=2,C=1)

if len(sys.argv) < 5:
    print("Usage: ./get_synonyms.py input_csv training_synonyms training_no-synonyms output [amount]")
    sys.exit()

input_csv = sys.argv[1]
training_syn = sys.argv[2]
training_ant = sys.argv[3]
output = sys.argv[4]
amount = 0
if len(sys.argv) == 6:
    amount = int(sys.argv[5])

features = ['pair','h1','h2','pagerank_difference','pagerank_sum','closeness_difference','self_neighbor_degree_ratio','shortest_distance','degree_ratio',
            'dispersion','clustering_sum','clustering_rate','closeness_sum','reciprocity','two_step_walks','betweenness_sum','betweenness_difference','clustering_difference'
            ,'degree_difference','degree_sum']

def string_to_features(elm):
    #elm[0] = int(elm[0])
    for i in range(0,len(elm)):
        elm[i] = float(elm[i])
    return elm

f = open(training_syn)
rd = csv.reader(f)
syn = []
for elm in rd:
    syn.append(string_to_features(elm))

f.close()
syn_values = ["syn" for i in syn]


f = open(training_ant)
rd = csv.reader(f)
ant = []
for elm in rd:
    ant.append(string_to_features(elm))

f.close()
ant_values = ["no-syn" for i in ant]

rfc.fit(syn+ant,syn_values+ant_values)


training_accuracy = rfc.score(syn+ant,syn_values+ant_values)
print("The training accuracy is: "+str(training_accuracy))

print("Trying to find synonyms now!")

f = open(input_csv)
rd = csv.reader(f)
rd.next() # Removing the head : P
found = 0
rejected = 0
count = 0
fout = open(output,'w')

for elm in rd:
    count += 1
    new_elm = elm[3:] # Removing labels
    res = rfc.predict(string_to_features(new_elm))
    if res[0] == "syn":
        #print("Found a synonym: "+elm[0])
        found += 1
        fout.write(elm[1]+','+elm[2]+'\n')
    else:
        rejected += 1

    if count == amount: break

print("Found a total of "+str(found)+" synonyms. Rejected "+str(rejected))
f.close()
fout.close()
