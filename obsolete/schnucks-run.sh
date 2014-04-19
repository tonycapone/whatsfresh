#!/bin/bash

cd /home/tony/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl schnucks
/home/tony/whatsfresh/pyscripts/schnucks-post.py