from scrapy import log
from scrapy.spider import BaseSpider

class WikipediaSpider(BaseSpider):
    name = "wikipedia"
    allowed_domains = ["wikipedia.com"]
    start_urls = (
        'http://www.wikipedia.com/',
        )

    def parse(self, response):
        self.log('A response from %s just arrived!'
                 % response.url)
