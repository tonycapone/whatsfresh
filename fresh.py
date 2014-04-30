#!/usr/bin/python

import sys
import fb.fbapp
import fb.pages
import emailsender
import bl
from storerun import *
import MySQLdb

    


def getfbposts():
    app = fb.fbapp.FBApp()
    pages = fb.pages.pages
    posts = []
    for page in pages.iteritems():
        posts.extend(app.getPosts(*page))
    
    conn = MySQLdb.connect(user='root', passwd='tidesof', db='whatsfresh', host='localhost', charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM `fbposts` WHERE 1""")
    conn.commit()
    for post in posts:
        id = post['id'].split('_')[1]
        try:
            cursor.execute("""INSERT INTO fbposts (id, link) VALUES (%s, %s)""", (id,post['link']))
            conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            continue
def main():
    
    func = getattr(sys.modules[__name__], sys.argv[1])
    func()
    
if __name__=='__main__':
    main()
