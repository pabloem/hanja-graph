from bs4 import BeautifulSoup
import requests
from urllib import quote


def _get_the_soup(url):
    r = requests.get(url)
    sp = BeautifulSoup(r.text)
    return sp

def get_word_txt(sp):
    word_txts = sp.select(".word_txt")
    related_hanja = -1
    for i,elm in enumerate(word_txts):
        if elm.select("h5")[0].text ==  u'\uad00\ub828 \ud55c\uc790': # "Related hanjas (gwallieon hanja)"
            return elm
    return None

def get_ems_text(elem):
    ems = elem.select("em")
    res = []
    for em in ems:
        res.append(em.text)
    return res

def get_from_title(wt,title):
    titles = wt.select("strong")
    for i,elm in enumerate(titles):
        if elm.text == title:
            return get_ems_text(wt.select("ul")[i])
    return []

def get_synonyms(wt):
    return get_from_title(wt,u'\uac19\uc740 \ub73b\uc744 \uac00\uc9c4 \ud55c\uc790') # Hanjas with the same meaning

def get_antonyms(wt):
    return get_from_title(wt,u'\ubc18\ub300 \ub73b\uc744 \uac00\uc9c4 \ud55c\uc790')# Hanjas with opposite meaning

def get_syn_ant(hanja):
    url_hanja = hanja.encode('utf-8')
    url_hanja = quote(url_hanja)
    url = 'http://hanja.naver.com/hanja?q='+url_hanja
    sp = _get_the_soup(url)

    wt = get_word_txt(sp)
    if wt is None:
        return None

    syn = get_synonyms(wt)
    ant = get_antonyms(wt)

    if len(syn) == 0 and len(ant) == 0:
        return None

    return {'hanja':hanja, 'synonyms':syn, 'antonyms':ant}
