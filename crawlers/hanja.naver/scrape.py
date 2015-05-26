from bs4 import BeautifulSoup
import requests
from hanja_datastore import hanja_datastore
from collections import deque
from urllib import quote
import json
import ipdb
from make_graph import make_bipartite_graph

class naver_scraper(object):
    def __init__(this,config):
        this.initial_hanja = config['initial_hanja']
        this._hanja_queue = deque();
        this._ds = hanja_datastore(config)
        this._max_pages_per_query = config['max_pages_per_query']
        this._url_prefix = config['url_prefix']
        this._hanja_prefix = config['hanja_url_prefix']
        this._scraped_hanjas = 0
        this._max_hanjas = config['max_hanjas']
        this._english_prefix = config['english_meaning_pref']
        this._requests = 0
        this.urls = []
        this._hanja_queue.append(this.initial_hanja)
        this._ds.addRootPlaceholder(this.initial_hanja)

    def _get_the_soup(this,url):
        this.urls.append(url)
        print("GETSOUP: Scraping page: "+url)
        r = requests.get(url)
        sp = BeautifulSoup(r.text)
        this._requests += 1
        return sp

    def _get_english(this,chinese, word_dic):
        print("GETENGL:Getting for " +str(word_dic))
        url_chinese = chinese.encode('utf-8')
        url_chinese = quote(url_chinese)
        url = this._english_prefix+url_chinese

        sp = this._get_the_soup(url)

        try:
            equivs = sp.select(".fnt_k05")[0].select(".EQUIV")
        except IndexError:
            print("Failed to get english meaning for: ", url_chinese);
        english = ""
        for i,equiv in enumerate(equivs):
            english = english + equiv.text +", "
        english = english[:-2]
        word_dic['english'] = english
        

    def scrape_word_query(this,character):
        url_options = "&searchOption=sortrank&ordr=dsc&pageNo="
        url_character = character.encode('utf-8')
        url_character = quote(url_character)

        for page_number in range(1,this._max_pages_per_query+1):
            scrape_url = (this._url_prefix+
                          url_character+
                          url_options+
                          str(page_number))

            sp = this._get_the_soup(scrape_url)

            try:
                words_dl = sp.select("#content")[0].select("dl")[0]
            except IndexError:
                print("SCRWRD: Couldn't find definitions in page")
                break
            hanja_dt = words_dl.select("dt")
            han_mean_dd = words_dl.select("dd")
            word_list = []
            
            for i,dt in enumerate(hanja_dt):
                ch = dt.text.strip()
                # We are using at most 4 character words
                if(len(ch) > 4):
                    print("SKIP:Char: "+ch)
                    continue
                word_list.append({'chinese':ch,
                                  'korean' : han_mean_dd[2*i].text.strip(),
                                  'meaning' : han_mean_dd[2*i+1].text.strip()})
                for hanja in ch:
                    if not this._ds.canAddToQueue(hanja):
                        continue
                    this._ds.addRootPlaceholder(hanja)
                    print("Adding "+hanja+" to the queue")
                    this._hanja_queue.append(hanja)
                    
            for i, wd in enumerate(word_list):
                this._ds.addWord(wd)
        this._scraped_hanjas += 1
        # Add the new words to the list
        # this._word_list = this._word_list + word_list

    def scrape_hanja(this,hanja):
        print("SCRHAN: Scraping hanja: "+hanja)
        url_hanja = hanja.encode('utf-8')
        url_hanja = quote(url_hanja)
        url = this._hanja_prefix+url_hanja
        sp = this._get_the_soup(url)
        
        pronunciation = sp.select("dd")[3].select("strong")[0].text
        pronunciation = pronunciation.split(",")[0].split()[-1]

        meaning = sp.select(".kinds_list")[0]
        meaning = meaning.select("ul")[0]
        meaning = meaning.select("li")[0].text[3:]
        short_meaning = meaning.split(",")[0].strip()

        hanja_dic = {'chinese' : hanja,
                     'pronunciation' : pronunciation,
                     'short_meaning' : short_meaning,
                     'meaning' : meaning}
        this._ds.addHanja(hanja_dic)

    def save_words(this,filename):
        out_list = []
        for w in this._ds._words:
            out_list.append(this._ds._words[w])
        f = open(filename,'w')
        f.write(json.dumps(out_list))

    def save_roots(this,filename):
        out_list = []
        for w in this._ds._hanja_data:
            out_list.append(this._ds._hanja_data[w])
        f = open(filename,'w')
        f.write(json.dumps(out_list))
                    
    def scrape(this):
        # The number of web requests here is about O(logn). This is fine.
        while (len(this._hanja_queue) > 0):
            try:
                hanja = this._hanja_queue.popleft()
                print("Getting "+hanja+" from the queue")
                this.scrape_hanja(hanja)
                if this._scraped_hanjas <= this._max_hanjas:
                    this.scrape_word_query(hanja)
            except:
                ipdb.set_trace()
        this._done_scrape = True

    def scrape_english_hanja(this):
        this._scrape_english(this._ds._hanja_data)

    def scrape_english(this):
        this._scrape_english(this._ds._words)

    def _scrape_english(this,dic):
        # The number of web requests here is O(n). This is not good.
        if not this._done_scrape:
            print("Should run a full 'chinese' scrape first.")
        for w in dic:
            try:
                word_dic = dic[w]
                this._get_english(word_dic['korean'],word_dic)
            except:
                pass

        # At this point we have all our words, and now we should get the english 


sc = naver_scraper({'initial_hanja' : u'\u5927',
                    'url_prefix':'http://hanja.naver.com/search/word?query=',
                    'hanja_url_prefix':'http://hanja.naver.com/hanja?q=',
                    'english_meaning_pref':'http://endic.naver.com/search.nhn?sLn=en&searchOption=entry_idiom&query=',
                    'max_hanjas': 3000,
                    'max_pages_per_query': 4,
                    'word_id': 'chinese'})

"""
The scraping process should be run as follows:
- Do NOT run unless knowing for sure what you're doing. This will run over 200,000 queries
on naver's dictionaries.
"""
sc.scrape()
#sc.scrape_english()
# sc.scrape_english_hanja()
#G = make_bipartite_graph(sc._ds._hanja_data,sc._ds._words)

