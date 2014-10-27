# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 18:00:25 2014

@author: pablo

The dtd specification of the graphml file format:
http://graphml.graphdrawing.org/dtds/graphml.dtd

Documentation for the etree.elementtree item of the python API
https://docs.python.org/2/library/xml.etree.elementtree.html
"""

from lxml import etree

def make_graphml_tree(words,hanjas,links):
    
    root = etree.Element("graphml",\
                        xmlns="http://graphml.graphdrawing.org/xmlns")
                        
    #root.append(etree.Element("key",id=str("chinese"), attr.name="chinese", attr.type="string"))
    root.append(etree.Element("key",id="chinese"))
    root[-1].set("for","node")
    root[-1].set("attr.type","string")
    root[-1].set("attr.name","chinese")
    
    root.append(\
        etree.Element("key",id="korean"))
    root[-1].set("for","node")
    root[-1].set("attr.type","string")
    root[-1].set("attr.name","korean")
    
    root.append(\
        etree.Element("key",id="english"))
    root[-1].set("for","node")
    root[-1].set("attr.type","string")
    root[-1].set("attr.name","english")
    
    root.append(\
        etree.Element("key",id="meaning"))
    root[-1].set("for","node")
    root[-1].set("attr.type","string")
    root[-1].set("attr.name","meaning")
    
    root.append(\
        etree.Element("key",id="label"))
    root[-1].set("for","node")
    root[-1].set("attr.type","string")
    root[-1].set("attr.name","label")
    
    root.append(\
        etree.Element("key",id="type"))
    root[-1].set("for","node")
    root[-1].set("attr.type","int")
    root[-1].set("attr.name","type")
    

    root.append(\
        etree.Element("graph", \
            id="BN_SinoKorean",\
            edgedefault="undirected"\
            )\
        )

    graph_node = root[-1]
  
    for word in words:
        graph_node.append(etree.Element("node",id=str(word['id'])))
        this_word = graph_node[-1]
        this_word.append(etree.Element\
                ("data",key="chinese"))#,attr.name="chinese"))
        this_word[-1].text=word['chinese']
        this_word.append(etree.Element("data",key="korean"))#,attr.name="korean"))
        this_word[-1].text=word['korean']
        this_word.append(etree.Element\
                ("data",key="english"))#,attr.name="english"))
        this_word[-1].text=word['english']
        this_word.append(etree.Element\
                ("data",key="label"))#,attr.name="label"))
        this_word[-1].text=word['label']
        this_word.append(etree.Element\
                ("data",key="type"))#,attr.name="type",attr.type="boolean"))
        this_word[-1].text="1"
        
    
    for hanja in hanjas:
        graph_node.append(etree.Element("node",id=str(hanja['id'])))
        this_word = graph_node[-1]
        this_word.append(etree.Element\
                ("data",key="chinese"))#,attr.name="chinese"))
        this_word[-1].text=hanja['chinese']
        this_word.append(etree.Element\
                ("data",key="label"))#,attr.name="label"))
        this_word[-1].text=hanja['label']
        this_word.append(etree.Element\
                ("data",key="meaning"))#,attr.name="meaning"))
        this_word[-1].text=hanja['label']
        this_word.append(etree.Element\
                ("data",key="type"))#,attr.name="type",attr.type="boolean"))
        this_word[-1].text=""
        
        
    
    for link in links:
        graph_node.append(etree.Element("edge",\
                        source=str(link['source']),\
                        target=str(link['target']),\
                        id=str(link['id'])\
                    ))
        
    return root
