# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DmozItem(Item):
    # define the fields for your item here like:
    title = Field()
    link = Field()
    desc = Field()

class TestItem(Item):
    id = Field()
    name = Field()
    description = Field()

class MyItem(Item):
    heading = Field()
    link = Field()
    body = Field()

class ScrapyItem(Item):
    title = Field()
    link = Field()
    content = Field()
