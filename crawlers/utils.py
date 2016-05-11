import requests
from bs4 import BeautifulSoup

def _get_the_soup(url):
    r = requests.get(url)
    sp = BeautifulSoup(r.text)
    return sp

def get_word_meaning(word):
    url = 'http://hanjadic.bravender.net/'+word
    sp = _get_the_soup(url)
    out_result = ""
    smWords = sp.select('.similar_words')
    if len(smWords) == 0:
        return out_result
    tr = smWords[0].select('tr')
    for tr in smWords:
        td = tr.select('td')[2]
        out_result += td.text.strip()
    return out_result

def get_hanja_meaning(hanja):
    #url_hanja = hanja.encode('utf-8')
    if len(hanja) > 1:
        return get_word_meaning(hanja)
    url = 'http://hanjadic.bravender.net/'+hanja
    sp = _get_the_soup(url)
    if len(sp.select('td')) > 1:
        return sp.select('td')[1].text
    return ''
