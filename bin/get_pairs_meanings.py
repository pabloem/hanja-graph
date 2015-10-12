#!/usr/bin/python
# Usage: ./get_synonyms.py input_csv training_csv output
import csv
import sys
from crawlers.utils import get_hanja_meaning

if len(sys.argv) < 3:
    print("Usage: ./get_pairs_meanings.py input_csv output [amount]")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
amount = 0
if len(sys.argv) == 4:
    amount = int(sys.argv[3])

f = open(input_file)
outf = open(output_file,'w')
cr = csv.reader(f)
#cw = csv.writer(outf)
count = 0

for elm in cr:
    count += 1
    hm1 = get_hanja_meaning(elm[0])
    hm2 = get_hanja_meaning(elm[1])
    str1 = elm[0]+" - "+hm1.encode('UTF-8')+"\n"
    outf.write(str1)

    str2 = elm[1]+" - "+hm2.encode('UTF-8')+"\n"
    outf.write(str2)
    outf.write("\n")
    if count % 50 == 0: print("Done "+str(count)+" pairs.")
    if count == amount: break

f.close()
outf.close()
