#!/usr/bin/env python

import os, sys, getopt, subprocess, time


#for checking/making remote crawl data dirtectory
def dir_check( rdir ):
	if not os.path.exists( rdir):
		os.makedirs( rdir)

print "Executing crawl..."

#for handling command line arguement
def main(argv):
	remote_dir='crawl_data'
	target='scrapy'
	try:
		opts, args = getopt.getopt(argv, "ht:d:", ["targ=","rcdir="])
	except getopt.GetoptError:
		print 'remote_python.py -t <target_script> -d <remote_crawl_directory>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'remote_python.py -t <target_script> -d <remote_crawl_directory>'
			sys.exit()
		elif opt in ('-d', '--rcdir'):
			remote_dir = arg
		elif opt in ('-t', '--targ'):
			target = arg

#	print 'Remote Crawl Directory is  : ', remote_dir
	dir_check(remote_dir)
	crawl_file = remote_dir + '/crawl_data.json'
	if os.path.exists(crawl_file):
		os.rename(crawl_file, crawl_file + '.' + str(int(time.time())))

	retcode = subprocess.call(["scrapy", "crawl", target, "-o", crawl_file, "-t", "json", "-a", "rdir="+remote_dir])

	print 'return code is :', retcode

if __name__ == '__main__':
	main(sys.argv[1:])


#if not os.path.exists

#scrapy crawl scrapy

print "Crawl completed..."


