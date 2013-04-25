#!/bin/bash

target_url="target_url"

sudo apt-get install apache2 httrack tshark

httrack $target_url -O "~/websites/remote_site" --mirrorlinks  -%v -r4 -%e0 -#L100000

sudo cp -r ~/websites/remote_site/* /var/www/

git clone git@github.com:SiddharthC/CCrawler.git

