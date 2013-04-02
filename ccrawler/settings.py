# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ccrawler'

SPIDER_MODULES = ['ccrawler.spiders']
NEWSPIDER_MODULE = 'ccrawler.spiders'

DEFAULT_REMOTE_DIR = 'crawl_data'
DEFAULT_SPIDER = 'base'
DEFAULT_URLS_LIST_FILE = 'urls.txt'
CRAWL_FILE_NAME = 'crawl_data.json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ccrawler (+http://www.yourdomain.com)'

