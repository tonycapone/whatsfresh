#!/usr/bin/python
import sys
from blogposttest import BlogPoster
from stores import stores

store = sys.argv[1]
print "Store is " + store
storepost = stores[store]


bpost = BlogPoster(storepost)
bpost.uploadpost()