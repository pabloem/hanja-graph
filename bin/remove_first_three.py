#!/usr/bin/python
import csv
import sys

if len(sys.argv) < 3:
    print("Usage: ./remove_first_three.py in_file output_file")

in_file = sys.argv[1]
out_file = sys.argv[2]

f = open(in_file)
rd = csv.reader(f)
res = []
for elm in rd:
    res.append(elm[3:])
f.close()

f = open(out_file,"w")
wr = csv.writer(f)
for elm in res:
    wr.writerow(elm)

f.close()
    
