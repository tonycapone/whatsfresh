#!/bin/bash

cd /home/tony/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl shopnsave
/home/tony/whatsfresh/pyscripts/shopnsave-post.py