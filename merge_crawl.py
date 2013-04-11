#!/usr/bin/env python

import os
import sys
import getopt
import subprocess
import time
import re

print "Starting crawl data merge..."

# for handling merging of existing crawl db


def merge_handler(remote_dir=None, crawldb=None):
    datafiles = [f for f in os.listdir(remote_dir) if isfile(join(remote_dir, f))]

    with open(crawldb, "a") as carwl_db:
        for f in datafiles:
            rfile = open(f, "r")
            tester = rfile.readline()
            
            #if its a valid remote file otherwise ignore
            if re.match('^<crawlRemoteURL>', tester):
                # Do coversion from local relative to absolute url
                url_info = re.search('<crawlRemoteURL>(.*)</crawlRemoteURL>', tester)
                if url_info:
                    # URL substring
#                    data_tmp = rfile.read()
#                    data_tmp.replace(localhost_something, url_info.group(1)) 
                    re.sub( '<id>(.*)/', url_info.group(1), rfile.read()) #TODO - Not checked probably done.
                    crawl_db.write(data_tmp)
                    rfile.close()
                    os.remove(f)                            # Work done so remove the file copied from remote.
            else:
                print 'File ' + f + ' contains invalid format. File will be skipped during merge. Please verify...'
            

# TODO do something that does the merging stuff...

# for handling command line arguement


def main(argv):
    remote_dir = 'remote_data'
    crawldb_dir = 'crawldb'
    try:
        opts, args = getopt.getopt(argv, "ht:d:", ["rdir=","ldir="])
    except getopt.GetoptError:
        print 'merge_crawl.py -t <directory_for_data_from_remote> -d <crawldb_directory>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'merge_crawl.py -t <directory_for_data_from_remote> -d <crawldb_directory>'
            sys.exit()
        elif opt in ('-d', '--ldir'):
            crawldb_dir = arg
        elif opt in ('-t', '--rdir'):
            remote_dir = arg

# for checking/making remote crawl data dirtectory
    if not os.path.exists(crawldb_dir):
        os.makedirs(crawldb_dir)
    crawldb_file = crawldb_dir + '/crawldb.json'

#	merging logic TODO

    merge_handler(remote_dir, crawldb_dir)

if __name__ == '__main__':
    main(sys.argv[1:])

print "Crawl data merge completed..."
