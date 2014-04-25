from fbtools import FB
import datetime
from pages import pages

class FBApp(object):
    def __init__ (self):
        
        self.fb = FB()
    def getPosts(self,name, username):
        log = []
        todayPosts = []
        posts = self.fb.getPosts(username)
        
        

        for post in posts:
            if post['created_time'] > (datetime.datetime.now() - datetime.timedelta(days=1)):
                
                post['created_time'] = post['created_time'].strftime("%m/%d/%Y")
                print post['created_time']
                
                todayPosts.append(post)
            else:
                return todayPosts
        

    
