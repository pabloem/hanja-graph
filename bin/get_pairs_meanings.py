#!/usr/bin/python3
import csv
import sys
from crawlers.utils import get_hanja_meaning

usage = """Usage: ./get_pairs_meanings.py input_csv output [amount]
Obtains the meanings of the pairs of words or characters that come from a CSV file. The amount can be limited."""
if len(sys.argv) < 3:
    print()
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
    str1 = elm[0]+" - "+hm1+"\n"
    outf.write(str1)

    str2 = elm[1]+" - "+hm2+"\n"
    outf.write(str2)
    outf.write("\n")
    if count % 50 == 0: print("Done "+str(count)+" pairs.")
    if count == amount: break

f.close()
outf.close()
