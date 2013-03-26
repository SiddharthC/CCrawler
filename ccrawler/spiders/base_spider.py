import os
import re
from urlparse import urljoin

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.shell import inspect_response

from ccrawler.items import BaseItem



class BaseSpider(BaseSpider):
    name = "base"
    start_urls = ()
    allowed_domains = []

    def __init__(self):
        # TODO: replace the root directory with constant or configuratoin value
        urls_list_path = os.path.join(os.path.dirname(__file__), "../../", "urls.txt")

        # Setting start_urls and allowed_domains from the urls.txt file,
        # located in <project>/urls.txt
        start_urls_list = []
        with open(urls_list_path, "r") as urls:
            for line in urls:
                if re.match("^#", line):
                    continue
                elif re.match("^http://", line):
                    start_urls_list.append(line.strip())
                else:
                    self.allowed_domains.append(line.strip())

        self.start_urls = tuple(start_urls_list)
        
    def parse(self, response):
        current_visit_url = response.url
        print ("Vistied: %s" % current_visit_url)

        # Just for debugging -------------------------------------------------------------
        # inspect_response(response) # Invoking the shell from spiders to inspect responses
        # ---------------------------------------------------------------------------------

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


        
