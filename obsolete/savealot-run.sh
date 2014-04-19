#!/bin/bash

cd /home/tony/storescraper/storescraper/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl savealot
/home/tony/whatsfresh/pyscripts/savealot-post.py