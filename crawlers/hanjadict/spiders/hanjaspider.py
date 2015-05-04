#from scrapy.spider import Spider
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from hanja.items import WordItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

##class HanjaSpider(Spider):
class HanjaSpider(CrawlSpider):
    name = "hanjaspider"
    allowed_domains = ["hanjadic.bravender.us"]
    start_urls = ["http://hanjadic.bravender.us/", "http://hanjadic.bravender.us/%E8%BB%8A"]
    rules = [Rule(SgmlLinkExtractor(allow=["\.+"]), callback='parse_words', follow = True)]

    def parse_words(self, response):
        items = []
        sel = Selector(response)
## Extract HANJAS
        hanjas = sel.xpath('//table[1]/tr')
        i = 0
        for hanja in hanjas:
            item = WordItem()
            item['wordType'] = 'hanja'
            item['chinese'] = ''.join(hanja.xpath('td[1]/a/text()').extract()).strip(' \t\n\r')
            item['meaning'] = ''.join(hanja.xpath('td[2]/text()').extract()).strip(' \t\n\r')
            if i == 0:
                radicals = ' '.join(sel.xpath('//div[@class="radicals"]/a/text()').extract()).strip(' \t\n\r')
                item['radicals'] = radicals
            i += 1
            items.append(item)

## Extract SIMILAR WORDS
        similar_words = sel.xpath('//table[2]/tr')
        for word in similar_words:
            item = WordItem()
            item['wordType'] = 'word'
            item['chinese'] = ''.join(word.xpath('td[1]/a/text()').extract()).strip(' \t\n\r')
            item['korean'] = ''.join(word.xpath('td[2]/text()').extract()).strip(' \t\n\r')
            item['english'] = ''.join(word.xpath('td[3]/text()').extract()).strip(' \t\n\r')
            items.append(item)
        return items
