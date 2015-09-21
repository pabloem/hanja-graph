from bs4 import BeautifulSoup
import requests

class MTKanjiScraper:
    def __init__(self,config):
        self._base = config['base_url']
        self._indexes = config['index_files']
        self._kanjis = []
        self._words = []
        self._wordSet = set()
        self._kanjiSet = set()
        self._missingKanji = set()
        self._linkDict = {}
        self._requests = 0
        pass

    def _get_the_soup(this,url):
        print("GETSOUP: Scraping page: "+url)
        r = requests.get(url)
        sp = BeautifulSoup(r.text)
        this._requests += 1
        return sp

    def scrape_kanji(self,kanji):
        res = {}

        url = self._base + self._linkDict[kanji]
        sp = self._get_the_soup(url)
        kanji = sp.select('h1')[0].text

        uls = sp.select('ul')
        li0 = uls[0].select('li')
        english = li0[0].text
        onyomi = li0[1].text
        kunyomi = li0[2].text

        res['chinese'] = kanji.strip()
        res['english'] = english.strip()
        res['onyomi'] = onyomi.strip()
        res['kunyomi'] = kunyomi.strip()
        self._kanjis.append(res)

        li1 = uls[1].select('li')
        li3 = uls[3].select('li')
        wordlis = li1 + li3
        for li in wordlis:
            wordRes = {}
            w_chinese = li.select('b')[0].text
            w_japanese = li.select('tt')[0].text
            w_english = li.select('i')[0].text
            extra = li.select('u')
            if len(extra) > 0:
                english = english+" "+extra[0].text
            wordRes['chinese'] = w_chinese.strip()
            wordRes['japanese'] = w_japanese.strip()
            wordRes['english'] = w_english.strip()
            if w_chinese in self._wordSet:
                continue
            for character in w_chinese:
                if character not in self._kanjiSet:
                    self._missingKanji.add(character)
            self._words.append(wordRes)
        

    def scrape_kanji_index(self,index_file):
        sp = self._get_the_soup(self._base+index_file)
        a_s = sp.select("a")[5:]
        i_s = sp.select("i")
        count = 0
        for i in range(len(a_s)):
            count += 1
            self._linkDict[a_s[i].text] = a_s[i]['href']
            self._kanjiSet.add(a_s[i].text)
        print("Got a total of: "+str(count))
        pass

    def go(self):
        for elm in self._indexes:
            self.scrape_kanji_index(elm)
        count = 0
        for kanji in self._linkDict:
            count += 1
            self.scrape_kanji(kanji)
            if count == 10: return

config = {'base_url':'http://www.manythings.org/kanji/d/',
          'index_files':['index.html']}#,'index2.html','index3.html','index4.html','index5.html']}
