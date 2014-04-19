
import MySQLdb
import emailsender
import datetime

class BlogPoster(object):
    def __init__(self, store):
        self.storestring = store['name']
        self.store = store
        
    def getposts(self):
        conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        cursor = conn.cursor();
        
        for op in self.store['departments']:
            cursor.execute("""SELECT * from store WHERE store = %s AND department LIKE %s""", (self.storestring, "%"+op+"%",))
        
            self.items = cursor.fetchall()
            self.procText(op)

    def uploadpost(self):
        self.subject = "%s Fresh deals at %s " % (datetime.datetime.now().strftime("%m/%d/%y"), self.storestring)
        self.postString=""
        self.getposts()
               
        emailsender.sendEmail(self.subject, self.postString)
        
    def procText(self, op):
        self.postString = self.postString + "%s \n\n" % op
        for row in self.items:
            
            uname = row[1]
            uprice = row[2]
            name = uname.encode('ascii', 'ignore')
            price = uprice.encode('ascii', 'ignore')
            
            
            self.postString = self.postString + name + '\t' + price + '\n'
        
        
        
        