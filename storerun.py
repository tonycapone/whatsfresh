#!/usr/bin/python
import sys
from bl.blogpost import BlogPoster
from stores import stores



def storerun(store):
    print "Store is " + store
    storepost = stores[store]


    bpost = BlogPoster(storepost)
    bpost.uploadpost()

if __name__ == '__main__':
    store = sys.argv[1]
    storerun(store)