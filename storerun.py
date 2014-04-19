#!/usr/bin/python
import sys
from bl.blogpost import BlogPoster
from stores import stores

store = sys.argv[1]
print "Store is " + store
storepost = stores[store]


bpost = BlogPoster(storepost)
bpost.uploadpost()