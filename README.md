CCrawler
========

A collaboration based crawling implementation focused at improving the overall crawling capability.

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
* To crawl the urls specified in urls.txt using base spider and generate a json file.

    $ ./fetch_crawl  # fetching pages and storing it in crawl_data folder
    
    
    $ ./update_solr  # Update json files in Solr.
    
    $ scrapy crawl base -o items.json -t json --nolog
    
    $ scrapy crawl base -o items.xml -t xml --nolog
