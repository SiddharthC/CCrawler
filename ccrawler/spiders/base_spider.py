import os
import re
import urllib2
import urllib

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
    items = []
    
    def __init__(self, rdir="remote_data", urlfile="urls.txt"):

	# create a remote directory if one does not exists
	if not os.path.exists("../../"+rdir):
            os.makedirs("../../"+rdir)

        # TODO: replace the root directory with constant or configuratoin value
        urls_list_path = os.path.join(
            os.path.dirname(__file__), "../../", urlfile)

        # Setting start_urls and allowed_domains from the urls.txt file,
        # located in <project>/urls.txt
        start_urls_list = []
        with open(urls_list_path, "r") as urls:
            for line in urls:
                if re.match("^#", line):
                    continue
                elif re.match("^http://", line):
        		current_visit_url = line.rstrip() 
        		# Checking is target file exists based on return code
                        try:
                            pre_crawldb_path = os.path.join(current_visit_url, 'ccdata/crawl_data.json')
                            # CHECKME: If urlopen tries to non-exist url, then it may raise an exception. 
                            ret = urllib2.urlopen(pre_crawldb_path)
                            if ret.code == 200:	#ccrawler file exists. Skip normal crawl...		
        			urllib.urlretrieve (pre_crawldb_path, "../../"+rdir+'/'+ (current_visit_url[6:]).replace('/', '.') + 'remote_crawl_data.json')
        			print("Crawl data found on target... Skipping crawling...")
        			continue
                        except: # file does not exists. Perform normal crawl... 
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
        title = hxs.select("//head/title/text()").extract()
        body = "".join(hxs.select('//div[contains(@class, "body")]//text()').extract())

        item = BaseItem()
        item['title'] = title
        item['link' ] = current_visit_url
        item['content'] = body
        self.items.append(item)

        links = hxs.select("//a/@href").extract()
        print("Links in %s" % current_visit_url)
        # for index, link in enumerate(links):
        # print("\t[%02d]: %s" %(index, urljoin(current_visit_url, link)))
        yield item
      
        if next_page:
            next_page = urljoin(current_visit_url, next_page[0])
            print ("\tnext_page -> %s" % next_page)
            yield Request(next_page, self.parse)

