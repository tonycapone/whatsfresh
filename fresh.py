#!/usr/bin/python

import sys
import fb.fbapp
import fb.pages
import bl
from storerun import *


    


def getfbposts():
    app = fb.fbapp.FBApp()
    pages = fb.pages.pages
    for page in pages.iteritems():
        app.getPosts(*page)
        
def main():
    
    func = getattr(sys.modules[__name__], sys.argv[1])
    func()
    
if __name__=='__main__':
    main()
