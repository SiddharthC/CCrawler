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
    try:
        opts, args = getopt.getopt(argv, "ht:d:u:", ["targ=", "rcdir=", "urlfile="])
    except getopt.GetoptError:
        print 'remote_python.py -t <target_script> -d <remote_crawl_directory> -u <url_file> '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'remote_python.py -t <target_script> -d <remote_crawl_directory> -u <url_file>'
            sys.exit()
        elif opt in ('-d', '--rcdir'):
            remote_dir = arg
        elif opt in ('-t', '--targ'):
            target = arg
        elif opt in ('-u', '--urlfile'):
            url_file = arg

#	print 'Remote Crawl Directory is  : ', remote_dir
    dir_check(remote_dir)
    crawl_file = os.path.join(remote_dir, CRAWL_FILE_NAME)
    if os.path.exists(crawl_file):
        os.rename(crawl_file, crawl_file + '.' + str(int(time.time())))

    retcode = subprocess.call(["scrapy", "crawl", target, "-o", crawl_file,
                              "-t", "json", "--nolog", "-a", "rdir="+remote_dir, "-a", "urlfile="+url_file])

    print 'return code is :', retcode

if __name__ == '__main__':
    main(sys.argv[1:])


# if not os.path.exists

# scrapy crawl scrapy

print "Crawl completed..."
