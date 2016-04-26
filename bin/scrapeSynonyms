#!/usr/bin/python

# This program, given a file with one hanja character per line, obtains
# their first appearing antonym and synonym.
import sys
from crawlers.antosyno.relatedWords import get_syn_ant

if len(sys.argv) < 4:
    print("Usage: ./sample_getter.py input_file antonyms_outfile synonyms_outfile")
    sys.exit()

input_file = sys.argv[1]
antonyms_outfile = sys.argv[2]
synonyms_outfile = sys.argv[3]


f = open(input_file)
res = []
for hanja in f:
    words = get_syn_ant(hanja.strip().decode('utf-8'))
    if words is not None:
        res.append(words)

f.close()

ant_file = open(antonyms_outfile,"w")

for elm in res:
    if len(elm['antonyms']) < 1:
        continue
    for i in range(len(elm['antonyms'])):
        first = elm['hanja'] if elm['hanja'] < elm['antonyms'][i] else elm['antonyms'][i]
        second = elm['hanja'] if elm['hanja'] >= elm['antonyms'][i] else elm['antonyms'][i]
        ant_file.write(first.encode("utf-8")+","+second.encode("utf-8")+"\n")

ant_file.close()

syn_file = open(synonyms_outfile,"w")

for elm in res:
    if len(elm['synonyms']) < 1:
        continue
    for i in range(len(elm['synonyms'])):
        first = elm['hanja'] if elm['hanja'] < elm['synonyms'][i] else elm['synonyms'][i]
        second = elm['hanja'] if elm['hanja'] >= elm['synonyms'][i] else elm['synonyms'][i]
        syn_file.write(first.encode("utf-8")+","+second.encode("utf-8")+"\n")

syn_file.close()
