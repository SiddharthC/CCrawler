from urlparse import urljoin
import logging
import os
import re
import urlparse

class UrlsManager:
    """ Manages urls list for crawling.
       
    """

    def __init__(self, allowed_domains = []):
        # The following urls list contains only full path.
        self.visited_urls = []
        self.urls_list = []
        self.allowed_domains = allowed_domains
        
    def url_normalize(self, url):
        # TODO URL Normalizer
        pass

    def add_urls(self, base_address, urls_list = [""], visited=False):
        """ add a url or list of urls and keep them in urls_list.
        
        base_address is a url of current page, so if ulrs_list contains relative urls, 
        full path could be made by joining it. urls_list could be a list of
        relative urls or absolute urls. Absolute urls start with 'http://' string.
        if visited is set True, then urls_list will be regarded as visited."""

        count = 0
        duplicated_count = 0
        ignored_count = 0
        
        web_extensions = [".html", ".htm", ".jsp", ".xml", ".aspx", ".cfm", ".chm", ".do", ".erb", ".htaccess", "mhtml", 
                         ".asp", ".mspx", ".php", ".php3", ".php4", ".phtml", ".php5", ".pl", ".py", ".seam", ".shtml", 
                         ".js", ".vbs", ".css"]
       
        # TODO: Normalize base address too -> URL.. 
        if base_address.find("#") >= 0:
            base_address = base_address[:base_address.find("#")] # # just pointing somewhere in the page
        path = urlparse.urlparse(base_address).path
        if os.path.splitext(path)[1] not in web_extensions:
            base_address = base_address.rstrip('/') # Normalization for urls ending with '/'
            base_address = base_address + "/"

        if isinstance(urls_list, str):
            urls_list = [urls_list] 
        for url in urls_list:
            # TODO: Normalize url, Refactoring.
            # Wiki Page's structure is a little bit comple, it contains. Chect that.

            if url.find("#") >= 0:
                url = url[:url.find("#")] # # just pointing somewhere in the page
            if "mailto:" in url:
                continue

            path = urlparse.urlparse(url).path
            extension = os.path.splitext(path)[1]
            if extension in [".txt"]:
                ignored_count += 1
                continue

            if not re.match("^https?://", url):
                url = urljoin(base_address, url)
                url = url.rstrip("/") # path/to/url and path/to/url/ should be same

            if extension not in web_extensions:
                if extension in [".png", ".jpg", ".jpeg", ".gif", ".mov", ".mp3", ".mpeg"]:
                    ignored_count += 1
                    continue
                
                url = url.rstrip("/") # path/to/url and path/to/url/ should be same
            
            url = unicode(url)
            
            if self.check_allowed_domain(url) is False:
                ignored_count += 1
                continue
            
            if url in self.visited_urls or url in self.urls_list or url + '/' in self.visited_urls or url + '/' in self.urls_list:
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
    
        logging.info("%d new urls are added, %d are ignored (%d ducplicated)." % (count, ignored_count, duplicated_count))
             
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
        print ("Visiting: %s" % url)
        return url
    
    def show_current_urls_status(self):
        logging.info ("URLS List%s\nVisited URLs%s" %(self.urls_list, self.visited_urls))

    def check_allowed_domain(self, url):
        """ Check the given url is in the allowed_domains.
        
        """ 
        
        allowed = False

        if len(self.allowed_domains) is 0:
            allowed = True
        else:   
            # TODO: Currently, the condition is not perfectly correct. It only looks substring of url.        
            for domain in self.allowed_domains:
                if domain in url:
                    allowed = True
            
        return allowed
            
    def update_allowed_domain(self, allowed_domains, reset=False):
        if reset is True:
            self.allowed_domains = allowed_domains
        else:
            self.allowed_domains.extend(allowed_domains)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    allowed_domains = ["example.com", "example.org", "google.com", "msn.com", "yahoo.com"]
    url_handler = UrlsManager(allowed_domains)
    url_handler.add_urls("http://www.google.com", "")
    url_handler.add_urls("http://www.google.com/", "")
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
    
    # check_allowed_domain
    assert(url_handler.check_allowed_domain("http://abc.example.com") == True)
    assert(url_handler.check_allowed_domain("http://www.example.com/example") == True)
    assert(url_handler.check_allowed_domain("http://abc.example.org") == True)
    assert(url_handler.check_allowed_domain("http://abc.example.edu") == False)
    
    url_handler.update_allowed_domain(["exampl.com"])
    assert(url_handler.check_allowed_domain("http://abcd.exampl.com") == True)
    url_handler.update_allowed_domain(["example.com"], True)
    assert(url_handler.check_allowed_domain("http://abcd.exampl.com") == False)
    