#!/usr/bin/env python

import os
import sys
import getopt
import subprocess
import time
import re

from ccrawler.settings import *

# for checking/making remote crawl data dirtectory
def dir_check(rdir):
    if not os.path.exists(rdir):
        os.makedirs(rdir)

print "Executing crawl..."

def merge_handler(remote_dir=DEFAULT_REMOTE_DIR):
    datafiles = [g for g in os.listdir(remote_dir+'/remote_data') if os.path.isfile(os.path.join(remote_dir+'/remote_data', g))]

    with open(remote_dir+'/crawl_data.json', "a") as crawl_db:
        for g in datafiles:
            subprocess.call(["tar", "-zxvf", remote_dir+'/remote_data/'+g, "-C", remote_dir+'/remote_data/'])
            g_splitted = g.split('.')
            f = g_splitted[0]+'.'+g_splitted[1]

            rfile = open(remote_dir+'remote_data/'+f, "r")
            tester = rfile.readline()

            #if its a valid remote file otherwise ignore
            if re.match('^<crawlRemoteURL>', tester):
                url_info = re.search('<crawlRemoteURL>(.*)</crawlRemoteURL>', tester)
                if url_info:
                    #print 'Url_info = '+ str(url_info)
                    data_tmp = rfile.read()
                    re.sub('<id>[\S]*//([\S]*?)/', url_info.group(1), data_tmp)
                    #print 'Data_dump = ' + data_tmp
                    crawl_db.write(data_tmp)
                    rfile.close()
                    os.remove(remote_dir+'/remote_data/'+f)
            else:
                print 'File ' + f + ' contains invalid format. File will be skipped during merge. Please verify...'

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
    if int(ccrawl_flag) == 1:
        merge_handler(remote_dir)
    else:
        subprocess.call(["tar", "-zcvf", crawl_file+'.tar.gz', crawl_file])

    print 'return code is :', retcode

if __name__ == '__main__':
    main(sys.argv[1:])


# if not os.path.exists

# scrapy crawl scrapy

print "Crawl completed..."
