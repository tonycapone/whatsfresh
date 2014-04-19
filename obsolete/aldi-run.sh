#!/bin/bash

cd /home/tony/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl aldi
/home/tony/whatsfresh/pyscripts/schnucks-post.py