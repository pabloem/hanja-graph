import requests
from bs4 import BeautifulSoup

def _get_the_soup(url):
    r = requests.get(url)
    sp = BeautifulSoup(r.text)
    return sp

def get_hanja_meaning(hanja):
    #url_hanja = hanja.encode('utf-8')
    url = 'http://hanjadic.bravender.net/'+hanja
    
    sp = _get_the_soup(url)
    if len(sp.select('td')) > 1:
        return sp.select('td')[1].text
    return ''
