import requests as r
from bs4 import BeautifulSoup
import time
from itertools import combinations
from selenium import webdriver


words = None
with open('chinese_words.csv') as f:
    words = [w.strip() for w in f]


baseUrl = "http://www.iciba.com/"

hdrs = {'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3'}
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


allComb = []
allSyn = []
allAnt = []

drv = webdriver.Firefox()

#nwI = 0
nwI = 18305
for i,w in enumerate(words):
    if i < nwI: continue
    if len(w) > 3: continue
    if i % 50 == 0: 
        print("Got {} words. Got {} combinations and {} synonyms. {} antonyms"
              .format(i+1,len(allComb),len(allSyn),len(allAnt)))
    pg = None
    gotIt = False
    while not gotIt:
        gotIt = True
        time.sleep(0.2)
        try:
            #pg = r.get(baseUrl+w,timeout=20,headers=hdrs)
            drv.get(baseUrl+w)
        except:
            gotIt = False
            print("Timed out. Retrying in 30.")
            time.sleep(30)

    #sp = BeautifulSoup(pg.text)
    sp = BeautifulSoup(drv.page_source)
    ow = sp.select(".opposite-word")
    if len(ow) == 0: continue
    art = ow[0].parent
    divs = art.select("div")
    if len(divs) == 0: continue

    synTime = True
    antTime = False
    wSyn = []
    wAnt = []
    for dv in divs:
        if dv.text == '同义词':
            synTime = True
            antTime = False
            continue
        if dv.text == '反义词':
            antTime = True
            synTime = False
            continue
        if synTime:
            synonym = dv.select_one('a').text
            wSyn.append(synonym)
            continue
        if antTime:
            antonym = dv.select_one('a').text
            wAnt.append(antonym)
            continue

    for ant in wAnt:
        allAnt.append([w,ant])
    for syn in wSyn:
        allSyn.append([w,syn])

    #wSyn.append(w)
    #allComb += list(combinations(wSyn,2))

with open("chinese_synonyms2_2.csv",'w') as f:
    wr = csv.writer(f)
    wr.writerows(allSyn)

with open("chinese_antonyms_2.csv",'w') as f:
    wr = csv.writer(f)
    wr.writerows(allAnt)

#with open("chinese_synonyms_2.csv",'w') as f:
#    wr = csv.writer(f)
#    wr.writerows(allComb)
