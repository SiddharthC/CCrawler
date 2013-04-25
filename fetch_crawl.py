#!/usr/bin/env python

import os
import sys
import getopt
import subprocess
import time

from ccrawler.settings import *

# for checking/making remote crawl data dirtectory
def dir_check(rdir):
    if not os.path.exists(rdir):
        os.makedirs(rdir)

print "Executing crawl..."

# for handling command line arguement
def main(argv):
    remote_dir = DEFAULT_REMOTE_DIR
    url_file = DEFAULT_URLS_LIST_FILE
    target = DEFAULT_SPIDER
    ccrawl_flag = DEFAULT_CCRAWL_FLAG
    try:
        opts, args = getopt.getopt(argv, "ht:d:u:c:", ["targ=", "rcdir=", "urlfile=","ccrawl_flag="])
    except getopt.GetoptError:
        print 'fetch_crawl.py -t <target_script> -d <remote_crawl_directory> -u <url_file> -c <ccrawl_flag(0 or 1)>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'fetch_crawl.py -t <target_script> -d <remote_crawl_directory> -u <url_file> -c <ccrawl_flag(0 or 1)>'
            sys.exit()
        elif opt in ('-d', '--rcdir'):
            remote_dir = arg
        elif opt in ('-t', '--targ'):
            target = arg
        elif opt in ('-u', '--urlfile'):
            url_file = arg
        elif opt in ('-c', '--ccrawl_flag'):
            ccrawl_flag = arg

#   print 'Remote Crawl Directory is  : ', remote_dir
    dir_check(remote_dir)
    crawl_file = os.path.join(remote_dir, CRAWL_FILE_NAME)
    if os.path.exists(crawl_file):
        os.rename(crawl_file, crawl_file + '.' + str(int(time.time())))

    retcode = subprocess.call(["scrapy", "crawl", target, "-o", crawl_file,
                              "-t", "json", "--nolog", "-a", "rdir="+remote_dir, "-a", "urlfile="+url_file, "-a", "ccrawl_flag="+ccrawl_flag])

    print 'return code is :', retcode

if __name__ == '__main__':
    main(sys.argv[1:])


# if not os.path.exists

# scrapy crawl scrapy

print "Crawl completed..."
