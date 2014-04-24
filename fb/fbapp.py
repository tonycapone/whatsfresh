from fbtools import FB
import datetime
from pages import pages

class FBApp(object):
    def __init__ (self):
        
        self.fb = FB()
    def getPosts(self,name, username):
        log = []
        posts = self.fb.getPosts(username)

        

        for post in posts:
            if post['created_time'] > (datetime.datetime.now() - datetime.timedelta(days=1)):
                log.append(name + '\n')
                log.append(post['created_time'].strftime("%m/%d/%Y") + '\n')
                print post['created_time']
                try:
                    log.append(post['message'] + '\n')
                except:
                    log.append("No message\n")
                log.append("link: " + post['link'] + '\n\n')
            else:
                return log
        

    
