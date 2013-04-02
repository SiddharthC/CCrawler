#!/usr/bin/env python
import os
import sys
import subprocess

from ccrawler.settings import *

def update_solr(argv, format='json'):
    if format != 'json':
        print("Currently only a json file is accepted.")
        return

    solr_json_path = 'http://localhost:8983/solr/update/json?commit=true'
    crawl_file_path = os.path.join(DEFAULT_REMOTE_DIR, CRAWL_FILE_NAME)

    # TODO: Recursive traverse the crawl data directory to update solr
    # Refer to http://wiki.apache.org/solr/UpdateJSON
    retcode = subprocess.call(["curl", solr_json_path, "--data-binary", 
                               "@%s" % crawl_file_path, "-H",
                               'Content-type:application/json'])
    print 'return code is :', retcode
    

if __name__ == '__main__':
    update_solr(sys.argv[1:])

