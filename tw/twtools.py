import tweepy

class Twitter(object):
    consumer_key = "LxjoN2oirrWXsKVoXkcAx00Gc"
    consumer_secret = "dEwNkHnU01zJOlenKUQEqYxVIAObC2lZLAaNYfEKQqhSA3bVZ3"
    key = "1631388444-15WRkF2LiTtSIGQGSUEs21SqEN3rkkXGUJUnzvC"
    secret = "2kUywBMHZfyFtfrZ3vAgGOA2KDD8NMXT0dpAUIDifeQrE"
    
    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.key, self.secret)
        self.api = tweepy.API(self.auth)
    
    def post(self, post):
        return self.api.update_status(post)
        