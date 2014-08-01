#!/bin/bash

Store=$1
echo $Store
cd /home/tony/whatsfresh/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl $Store
/home/tony/whatsfresh/storerun.py $Store