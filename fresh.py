#!/usr/bin/python

import sys
from fb import *
from bl import *
from storerun import *

def main():
    getattr('fresh', func)
    func()
    
if __name__=='__main__':
    main()

def getfbposts():
    app = FBApp()
    for page in pages.iteritems():
        app.getPosts(*page)
    

