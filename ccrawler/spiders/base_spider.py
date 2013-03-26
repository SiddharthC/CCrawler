from urlparse import urljoin

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.shell import inspect_response

from ccrawler.items import BaseItem


class BaseSpider(BaseSpider):
    name = "base"
    allowed_domains = ["scrapy.org"]
    start_urls = (
        'http://doc.scrapy.org/en/0.16/',
        )

    def parse(self, response):
        current_visit_url = response.url
        print ("Vistied: %s" % current_visit_url)

#        inspect_response(response) # Invoking the shell from spiders to inspect responses

        hxs = HtmlXPathSelector(response)
        next_page = hxs.select("//html/body/div[3]/ul/li[3]/a/@href").extract()

        body = "".join(hxs.select('//div[contains(@class, "body")]//text()').extract())
        print(body)

        links = hxs.select("//a/@href").extract()

        print("Links in %s" % current_visit_url)
        for index, link in enumerate(links):
            print("\t[%02d]: %s" %(index, urljoin(current_visit_url, link)))

        
        if not not next_page:
            next_page = urljoin(current_visit_url, next_page[0])
            print ("\tnext_page -> %s" % next_page)
            yield Request(next_page, self.parse)


        
