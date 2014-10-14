# -*- coding: utf-8 -*-
"""
Start basic configuration
    1. Import libraries
    2. Set up logging
        Levels: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
"""
import logging
import json
import sys
import gexf_maker
import graphml_maker
from lxml import etree

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.basicConfig(stream=sys.stderr, leval=logging.NOTSET)


# Change directory %cd /home/pablo/codes/hanja/def_lists/
file = open("def_lists/hanja_list.json")
hanjas = json.loads(file.read())

file= open("def_lists/words.nospace.json")
words = json.loads(file.read())

"""
# First we make sure to have unique, different words in each word item.
# If the words repeat then the graph is not optimal
# A PROBLEM WITH THIS APPROACH IS THAT THERE ARE REPEATED ITEMS IN THE ENGLISH
# MEANING OF A LOT OF WORDS. THAT CAN BE FIXED.
"""


chinkor = []
new_words = []
for word in words:
    if word['chinese']+word['korean'] not in chinkor:
        new_words.append(word)
        chinkor.append(word['chinese']+word['korean'])
    else:
        for item in new_words:
            if item['chinese']+item['korean']==word['chinese']+word['korean']:
                item['english'] = item['english']+' '+word['english']
                #print 'Modifying the item ', item['korean'], 'into :', \
                #    item['english']

print 'Reduced the original list from ', len(words), ' words to ', \
    len(new_words), ' words'
    
words = new_words

del word
del item
del new_words
del chinkor

"""
Time to uniquify the words in a list
"""

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

i = 0
for word in words:
    logging.debug('Simplifying '+word['english'])
    word['english'] = u' '.join(unique_list(word['english'].split()))
    logging.debug('Simplified '+word['english'])
#    i = i+1
#    if i%10 == 0:
#        raw_input('Press enter...')
    

del word

new_hanjas = []
hanja_codes = []
for hanja in hanjas:
    if hanja['chinese'] not in hanja_codes:
        hanja_codes.append(hanja['chinese'])
        new_hanjas.append(hanja)

print 'Reduced the original list from ', len(hanjas), ' chinese characters to '\
    , len(new_hanjas), ' individual chinese characters'

hanjas = new_hanjas

del hanja
del new_hanjas
del hanja_codes

# Adding id to the words and chinese characters
id = 1
for word in words:
    word['id'] = id
    word[u'label'] = 'W-'+word['korean']+word['english'].split()[0]
    word[u'type'] = "TRUE"
    id = id+1
for hanja in hanjas:
    hanja['id'] = id = id+1
    hanja[u'label'] = 'H-'+hanja['chinese']+hanja['meaning']

del word
del hanja

"""
Here is the most important step: Compute the list of links
"""

links = []
current_id = 0
for hanja in hanjas:
    logging.info('Hanja is: '+str(hanja))
    for word in words:
        if hanja['chinese'] in word['chinese']:
            new_link = {'id':current_id, 'source':hanja['id'], \
                'target':word['id']}
            links.append(new_link)
            logging.debug('New link:'+str(new_link))
            del new_link
            current_id = current_id + 1
            logging.info('Found '+str(current_id)+' links up to '\
                + hanja['chinese'])
print 'Found a total ', current_id, ' links'

"""
At this point, we have the list of links and nodes (hanjas and words).
Now we just need to output as xml, in a valid format
"""

#xml_tree = gexf_maker.make_gexf_tree(words,hanjas,links)
xml_tree = graphml_maker.make_graphml_tree(words,hanjas,links)

#outfile = open('output.gexf','w+')
outfile = open('output.graphml','w+')
outfile.write(etree.tostring(xml_tree,pretty_print=True,encoding='unicode'))
outfile.close()