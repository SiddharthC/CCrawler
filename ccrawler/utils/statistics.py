'''
Created on Apr 25, 2013

'''
from scrapy import project, signals
from scrapy.xlib.pydispatch import dispatcher
import logging
import time


class Statistics:
    """ It measures Per page crawling time, transfer size, Per request time, etc.
    
    """ 
    request_time = float()
    response_time = float()
    download_time = float()
    total_download_time = 0.0 # in ms
    total_elapsed_time = 0.0 # in ms
    total_response_size = 0 # in byte
    total_number_of_urls = 0 # TODO: First URL is ignored for now.
   
    url = None
    stat_data = []
    start_time_checked = False
    
    def _init_(self):
        pass
    
    def item_request_received(self, request, spider):
        self.request_time = time.time()
        logging.info("Request time: %f" % self.request_time)
        self.url = request.url
        self.start_time_checked = True

    def item_response_downloaded(self, response, request, spider):
        self.download_time = time.time()
        logging.info("Download time: %f" % self.download_time)

    def item_response_received(self, response, request, spider):
        self.response_time = time.time()
        logging.info("Response time: %f" % self.response_time)
        if self.url == response.url and self.start_time_checked is True:
            download_time = self.get_item_download_time() * 1000.0
            elapsed_time = self.get_item_elapsed_time() * 1000.0
            logging.info("Elpased Downloaded time %0.2f ms" % download_time)        
            logging.info("Elapsed time: %0.2f ms\n" % elapsed_time)
            # https://scrapy.readthedocs.org/en/latest/topics/autothrottle.html?highlight=latency
            # latency - the time elapsed between establishing the TCP connection and receiving the HTTP headers
            self.total_download_time += download_time
            self.total_elapsed_time += elapsed_time
            self.total_number_of_urls += 1
            self.total_response_size += len(response.body)
            # url, request_size, download_latency, download_time, elapsed_time, 
            stat = (self.url, len(response.body), response.meta['download_latency'], download_time, elapsed_time)
            self.stat_data.append(stat)
            logging.info(stat)
         
        self.start_time_checked = False

    
    def get_item_elapsed_time(self):
        if self.start_time_checked is True:
            elapsed_time = (self.response_time - self.request_time)
        else:
            print ("Ignore this time. it doesn't have start time yet.")
            elapsed_time = 0.0
        return elapsed_time

    def get_item_download_time(self):
        if self.start_time_checked is True:
            elapsed_time = (self.download_time - self.request_time)
        else:
            print ("Ignore this time. it doesn't have start time yet.")
            elapsed_time = 0.0
        return elapsed_time

    def get_summary(self):
        stat_summary = (self.total_number_of_urls, self.total_response_size, self.total_download_time, self.total_elapsed_time)
        print ("Total # of URLs: %d\nTotal Response size: %d bytes\nTotal Downloadtime: %.2f ms\nTotal Elapsed Time: %.2f ms" %
               stat_summary)
        print ("Average Elapsed Time: %.2f ms" % (self.total_elapsed_time / self.total_number_of_urls))
        print ("Average Resonse Size: %.2f bytes" % (self.total_response_size / float(self.total_number_of_urls)))
        return stat_summary