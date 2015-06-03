import re
class hanja_datastore(object):
    def __init__(this,config):
        this._words = {}
        this._roots = set()
        this._hanja_data = {}
        this._word_id = config['word_id']
        this._chinese_re = re.compile(u'[\u4E00-\u9FFF|\u2FF0-\u2FFF|\u31C0-\u31EF|\u3200-\u9FBF|\uF900-\uFAFF]',re.UNICODE)

    def canAddToQueue(this,root):
        return root not in this._roots and this._chinese_re.match(root)

    def addHanja(this,hanja_dic):
        this._hanja_data[hanja_dic[this._word_id]] = hanja_dic
    
    def addWord(this, word):
        if word[this._word_id] in this._words:
            return
        this._words[word[this._word_id]] = word
        this.addRootPlaceholder(word[this._word_id])

    def addRootPlaceholder(this,word):
        for rt in word:
            if rt in this._roots:
                continue
            this._roots.add(rt)

    
