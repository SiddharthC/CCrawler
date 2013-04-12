import re
import logging
import os
from urlparse import urljoin

class UrlsManager:
    """ Manages urls list for crawling.
       
    """

    def __init__(self):
        # The following urls list contains only full path.
        self.visited_urls = []
        self.urls_list = []

    def add_urls(self, base_address, urls_list = [""], visited=False):
        """ add a url or list of urls and keep them in urls_list.
        
        base_address is a url of current page, so if ulrs_list contains relative urls, 
        full path could be made by joining it. urls_list could be a list of
        relative urls or absolute urls. Absolute urls start with 'http://' string.
        if visited is set True, then urls_list will be regarded as visited."""

        count = 0
        duplicated_count = 0
        if isinstance(urls_list, str):
            urls_list = [urls_list] 
        for url in urls_list:
            if not re.match("^http://", url):
                url = urljoin(base_address, url)
            if url in self.visited_urls or url in self.urls_list:
                duplicated_count += 1
                logging.debug("%s is already visited." % url)
                continue
            if visited is False:
                logging.debug("%s is newly added." % url)
                self.urls_list.append(url)
            else:
                logging.debug("%s is newly added as visited." % url)
                self.visited_urls.append(url)
                logging
            count += 1
        
        logging.info("%d new urls are added, %d are ignored." % (count, duplicated_count))
             
    def get_next_url(self):
        """ Retrieve next url from urls_list..
        
        It doesn't care about the order to retrieve, however it will not return the url which was already visited.
        None will be returned if there is no more url in the list.
        """
        url = None
        
        if len(self.urls_list) <= 0:
            logging.info("No more urls.")
            return url
        
        while len(self.urls_list) > 0:
            url = self.urls_list.pop()
            if url in self.visited_urls:
                url = None
                continue
            else:
                self.visited_urls.append(url)
                break
            
        return url
    
    def show_current_urls_status(self):
        logging.info ("URLS List%s\nVisited URLs%s" %(self.urls_list, self.visited_urls))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    url_handler = UrlsManager()
    url_handler.add_urls("http://www.google.com", "")
    url_handler.add_urls("http://msn.com")
    url_handler.add_urls("http://www.google.com", ["patent", "scholar"])
    print url_handler.get_next_url()
    url_handler.add_urls("http://www.google.com", "patent")
    url_handler.add_urls("http://www.example.com", ["abc", "def", "xyz"])
    
    # The following addresses should not be printed out
    url_handler.add_urls("http://yahoo.com", ["xyz", "wxy"], visited=True)

    print url_handler.get_next_url()
    print url_handler.get_next_url()
    print url_handler.get_next_url()
    print url_handler.get_next_url()
    print url_handler.get_next_url()
    print url_handler.get_next_url()

    assert (url_handler.get_next_url() == None)