#!/bin/bash

cd /home/tony/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl wholefoods
/home/tony/whatsfresh/pyscripts/wholefoods-post.py