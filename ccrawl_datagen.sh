#!/bin/bash

# script to run the crawl for 4 different clients - simple implementation
# used to generate data at nodes.

fetch_crawl.py -t base -d url1/ -u url1/urls.txt &
fetch_crawl.py -t base -d url2/ -u url2/urls.txt &
fetch_crawl.py -t base -d url3/ -u url3/urls.txt &
fetch_crawl.py -t base -d url4/ -u url4/urls.txt &
