import csv
from collections import Counter
import regex as re

f = open('chinesegraph/words.txt')
words = list(csv.reader(f))

minHan = u'\u4e00'
maxHan = u'\u4dff'

weirdChars = []

pattern = re.compile(r'([\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)', re.UNICODE)

for w in words:
    w = w[0]
    for ch in w:
        if pattern.match(ch) is None:
            weirdChars.append(ch)

wc = Counter(weirdChars)

nwW = []
for w in words:
    w = w[0]
    good = True
    for ch in w:
        if ch in wc: good = False
    if good: nwW.append(w)

nwW = [w for w in nwW if len(w) <= 5]

with open('chinese_words.csv','w') as f:
    for w in nwW:
        f.write(w+'\n')

