from scrapy.spider import BaseSpider

class ExampleSpider(BaseSpider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = (
        'http://www.example.com/',
        )

    def parse(self, response):
        pass 
