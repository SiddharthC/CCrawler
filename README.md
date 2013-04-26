CCrawler
========

An implementation of collaboration based crawling approach focused at improving the overall crawling capability.

Project URL: https://github.com/SiddharthC/CCrawler
------------

Structures
--------
    .                             - <project root>
    ├── ccrawler                  - collaborative crawler implementation directory
    │   ├── settings.py	          - default constant variables defined
    │   └── spiders               - spider directory
    │       └── base_spider.py    - base spider implementation
    ├── items.json                - a (temporary) json file containing crawled data (title, link, content)
    ├── fetch_crawl.py
    ├── merge_crawl.py
    ├── remote_crawl.py
    ├── update_solr.py            - update Solr with json files
    ├── schema.xml                - Put this file in to Solr conf directory
    ├── scrapy.cfg                - project configuration 
    └── urls.txt                  - urls list file containing an allowed domain and start urls


Run
--------

# To crawl the urls specified in urls.txt using a spider and to store the generated data at a specified location as a json file.
$ ./fetch_crawl -t <spider_name> -d <location_to_store_data> -u <path_to_url_file> -c <collaborative_crawling_flag (0 or 1)>

# Update json file in Solr       
$ ./update_solr  # Update json files in Solr.
    
# Standalone crawling by spider to store data as json
$ scrapy crawl base -o items.json -t json --nolog
    
# Standalone crawling by spider to store data as xml
$ scrapy crawl base -o items.xml -t xml --nolog