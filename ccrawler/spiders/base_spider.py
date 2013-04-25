import os
import re
import urllib2
import urllib
import time
import logging

from urlparse import urljoin
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.shell import inspect_response
from ccrawler.items import BaseItem

from ccrawler.settings import *
from ccrawler.utils.urls_manager import UrlsManager

class BaseSpider(BaseSpider):
    name = DEFAULT_SPIDER
    start_urls = ()
    allowed_domains = []
    items = []
    handle_httpstatus_list = [404]


    def __init__(self, rdir="remote_data", urlfile=DEFAULT_URLS_LIST_FILE, ccrawl_flag=DEFAULT_CCRAWL_FLAG):

        # create a remote directory if one does not exists
        if not os.path.exists(rdir):
                os.makedirs(rdir)
                
        # TODO: replace the root directory with constant or configuratoin value
        urls_list_path = os.path.join(
            os.path.dirname(__file__),'../../', urlfile)

        # Setting start_urls and allowed_domains from the urls.txt file,
        # located in <project>/urls.txt
        start_urls_list = []
        self.urls_manager = UrlsManager()
        
        with open(urls_list_path, "r") as urls:
            for line in urls:
                if re.match("^#", line):
                    continue
                elif re.match("^https?://", line):
                    current_visit_url = line.rstrip()
                    if int(ccrawl_flag) == 1:
                        if not os.path.exists(rdir+'/remote_data'):
                            os.makedirs(rdir+'/remote_data')
                        #p = re.compile('^[\S]*?\/\/[\S]*?\/')
                        url_splitted = current_visit_url.split('/')
                        #print url_splitted[0]+'//'+url_splitted[2]+'/'+url_splitted[3]+'/'
                        # Checking is target file exists based on return code
                        try:
                            pre_crawldb_path = os.path.join(url_splitted[0]+'//'+url_splitted[2]+'/'+url_splitted[3]+'/', 'ccdata', CRAWL_FILE_NAME+'.tar.gz')
                            # CHECKME: If urlopen tries to non-exist url, then it may raise an exception. 
                            ret = urllib2.urlopen(pre_crawldb_path)
                            if ret.getcode() == 200:  # ccrawler file exists. Skip normal crawl...
                                rcopy_local = open(rdir+'/remote_data/' + 'remote_crawl_data-' + str(
                                   int(time.time())) + '.json.tar.gz', 'w')
                                rcopy_local.write('<crawlRemoteURL>' + current_visit_url + '</crawlRemoteURL>\n')
                                rcopy_local.write(ret.read())
                                rcopy_local.close()
                                print("Crawl data found on target...\nSkipping crawling...\n")
                                continue
                        except: # file does not exists. Perform normal crawl... 
                            start_urls_list.append(line.strip())
                    else:
                        start_urls_list.append(line.strip())

                else:
                    if len(line.strip()) > 0:
                        self.allowed_domains.append(line.strip())

        self.start_urls = tuple(start_urls_list)
        self.urls_manager.update_allowed_domain(self.allowed_domains)
        self.urls_manager.add_urls("", start_urls_list, visited=True)
        
    def parse(self, response):
        current_visit_url = response.url
        logging.info ("Vistied: %s" % current_visit_url)

        if response.status != 404:
            # Just for debugging -------------------------------------------------------------
            # inspect_response(response) # Invoking the shell from spiders to inspect responses
            # ---------------------------------------------------------------------------------
            try:
                hxs = HtmlXPathSelector(response)
                anchors = hxs.select("//a")
                next_candidate_urls = anchors.select("@href").extract()
                title = hxs.select("//head/title/text()").extract()
                body = "".join(hxs.select('//body/text()').extract())
        
                item = BaseItem()
                item['id'] = current_visit_url
                if title:
                    item['title'] = title[0]
                item['content'] = body
                link_infos = []
                for anchor in anchors:
                    link_info = (anchor.select("text()").extract(), anchor.select("@href").extract())
                    link_infos.append(link_info)
                item['links'] = link_infos
        #        item['link' ] = current_visit_url
                self.items.append(item)
        
                # links = hxs.select("//a/@href").extract()
                # print("Links in %s" % current_visit_url)
                # for index, link in enumerate(links):
                # print("\t[%02d]: %s" %(index, urljoin(current_visit_url, link)))
                yield item

                if next_candidate_urls:
                    self.urls_manager.add_urls(current_visit_url, next_candidate_urls)

            except AttributeError:
                # TODO: This exception is due to requesting "~.png", but it doesn't know how to handle it.
                logging.info("Exception Occurs! while parsing.")
                next_url = self.urls_manager.get_next_url()
                
                if next_url is not None:
                    logging.info ("\tnext_url -> %s" % next_url)
                    yield Request(next_url, self.parse, errback=self.base_errback)          
                

    
            logging.debug(self.urls_manager.show_current_urls_status())
            
        else:
            logging.info("Return status 404: %s", current_visit_url)
        
        next_url = self.urls_manager.get_next_url()
        
        if next_url is not None:
            logging.info ("\tnext_url -> %s" % next_url)
            yield Request(next_url, self.parse, errback=self.base_errback, dont_filter = True)          

    def base_errback(self, failure):
        logging.info("Error occurs")
        next_url = self.urls_manager.get_next_url()
        
        if next_url is not None:
            logging.info ("\tnext_url -> %s" % next_url)
            yield Request(next_url, self.parse, errback=self.base_errback, dont_filter = True)          

        
