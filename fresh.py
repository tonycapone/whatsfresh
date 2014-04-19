#!/usr/bin/python

import sys
import fb.fbapp
import fb.pages
import emailsender
import bl
from storerun import *


    


def getfbposts():
    app = fb.fbapp.FBApp()
    pages = fb.pages.pages
    posts = []
    for page in pages.iteritems():
        posts.extend(app.getPosts(*page))
    
    
    emailsender.sendEmail("Today's FB Posts", ' '.join(posts), "anthony.r.howell@gmail.com")
    
def main():
    
    func = getattr(sys.modules[__name__], sys.argv[1])
    func()
    
if __name__=='__main__':
    main()
