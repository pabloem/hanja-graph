#!/usr/bin/python
import sys
from crawlers.antosyno.relatedWords import get_syn_ant

if len(sys.argv) < 2:
    print("# Usage: ./sample_tester.py input.json")
    sys.exit(0)

input_file = sys.argv[1]
f = open(input_file)

correct = 0
count = 0
for elm in f:
    elm = elm.decode('utf-8').strip()
    h1 = elm[0]
    h2 = elm[1]
    syn1 = get_syn_ant(h1)
    syn2 = get_syn_ant(h2)
    count += 1
    if ((syn2 is not None and h1 in syn2['synonyms']) or 
        (syn1 is not None and h2 in syn1['synonyms'])): 
        correct += 1
        print(elm)
    if count % 1000 == 0: print("Tested "+str(count)+" pairs.")

print("Count: "+str(count)+" | Correct: "+str(correct))

f.close()
