#!/bin/bash

target_url="target_url"

sudo apt-get install apache2 httrack tshark

httrack $target_url -O "~/websites/remote_site" --mirrorlinks  -%v -r4 -%e0 -#L1000

sudo cp -r ~/websites/remote_site/* /var/www/

git clone git@github.com:SiddharthC/CCrawler.git


#set up the crawler and run it between durations of this 

#sudo tshark -i lo -f "port 80" -a duration:60 -z conv,ip -q
