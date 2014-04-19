from fbtools import FB
import datetime
from pages import pages

class FBApp(object):
    def __init__ (self):
        
        self.fb = FB()
    def getPosts(self,name, username):
        log = open("log.txt", 'a')
        posts = self.fb.getPosts(username)

        

        for post in posts:
            if post['created_time'] > (datetime.datetime.now() - datetime.timedelta(days=1)):
                log.write(name + '\n')
                log.write(post['created_time'].strftime("%m/%d/%Y") + '\n')
                try:
                    log.write(post['message'] + '\n')
                except:
                    log.write("No message\n")
                log.write("link: " + post['link'] + '\n\n')
            
        log.close()
        

    
