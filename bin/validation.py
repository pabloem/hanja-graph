#!/usr/bin/env python
import sys
import csv

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

usage = "Usage: ./validation.py training_validate training_no-synonyms output [-e #]"
if len(sys.argv) < 4:
    print(usage)
    sys.exit(0)

syn_f = open(sys.argv[1])
nosyn_f = open(sys.argv[2])
outf = open(sys.argv[3],'w')

n = 50
if len(sys.argv) > 5:
    n = int(sys.argv[5])

def string_to_features(elm):
    #elm[0] = int(elm[0])
    for i in range(0,len(elm)):
        elm[i] = float(elm[i])
    return elm

syn = [string_to_features(rw) for rw in csv.reader(syn_f)]
syn_val = ["syn" for _ in syn]
syn_f.close()

nosyn = [string_to_features(rw) for rw in csv.reader(nosyn_f)]
nosyn_val = ["no-syn" for _ in nosyn]


diff = 0
for i in range(0,len(syn),n):
    rfc = AdaBoostClassifier(base_estimator=RandomForestClassifier())
    train = syn[0:i]+syn[i+n:len(syn)] + nosyn
    train_v = syn_val[:-n] + nosyn_val
    rfc.fit(train,train_v)

    test = syn[i:i+n]
    prob = rfc.predict_proba(test)
    for elm in prob:
        pr = elm[1]
        outf.write(str(pr)+'\n')
        diff += 1
    if diff > 50:
        print("Done a total of "+str(i+1))
        diff = 0






