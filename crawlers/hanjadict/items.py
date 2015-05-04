# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WordItem(Item):
    wordType = Field()
    chinese = Field()
    korean = Field()
    english = Field()
    meaning = Field()
    radicals = Field()
    pass

