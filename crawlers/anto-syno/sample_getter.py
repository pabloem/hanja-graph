#!/usr/bin/python
import sys
from relatedWords import get_syn_ant

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
    first = elm['hanja'] if elm['hanja'] < elm['antonyms'][0] else elm['antonyms'][0]
    second = elm['hanja'] if elm['hanja'] >= elm['antonyms'][0] else elm['antonyms'][0]
    ant_file.write(first.encode("utf-8")+","+second.encode("utf-8")+"\n")

ant_file.close()

syn_file = open(synonyms_outfile,"w")

for elm in res:
    if len(elm['synonyms']) < 1:
        continue
    first = elm['hanja'] if elm['hanja'] < elm['synonyms'][0] else elm['synonyms'][0]
    second = elm['hanja'] if elm['hanja'] >= elm['synonyms'][0] else elm['synonyms'][0]
    syn_file.write(first.encode("utf-8")+","+second.encode("utf-8")+"\n")

syn_file.close()
