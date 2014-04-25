import facebook
import datetime

class FB(object):
    def __init__(self):
        self.appID = "1414708192129481"
        self.secret = "b657972c7c6d4d007641e2f89df4ba02"
        self.graph = facebook.GraphAPI()
        self.key = self.graph.get_app_access_token(self.appID, self.secret)
        
        self.graph.access_token = self.key
        print self.graph.access_token
        #self.me = self.graph.get_object("me")
    
    def getPosts(self, profileStr):
        
        profile = self.graph.get_object(profileStr)
        feed = self.graph.get_connections(profile['id'], "posts")
        for post in feed['data']:
            post["link"] = self.parseLink(post["id"],profileStr)
            post["created_time"] = datetime.datetime.strptime(
                post["created_time"], "%Y-%m-%dT%H:%M:%S+0000") 
            yield post
    def parseLink(self, post, profileStr):
        
        postid = post.split('_')
        link = "https://www.facebook.com/%s/posts/%s" % (profileStr,postid[1])
        return link
        