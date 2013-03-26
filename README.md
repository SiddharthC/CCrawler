CCrawler
========

A collaboration based crawling implementation focused at improving the overall crawling capability.

Structures
--------
    .                             - <project root>
    ├── ccrawler                  - collaborative crawler implementation directory
    │   └── spiders               - spider directory
    │       └── base_spider.py    - base spider implementation
    ├── items.json                - a (temporary) json file containing crawled data (title, link, content)
    ├── remote_crawl.py
    ├── scrapy.cfg                - project configuration 
    └── urls.txt                  - urls list file containing an allowed domain and start urls


Run
--------
* To crawl the urls specified in urls.txt using base spider and generate a json file.

    $ scrapy crawl base -o items.json -t json --nolog
