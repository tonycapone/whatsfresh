
import MySQLdb
import emailsender
import datetime

class BlogPoster(object):
    filters = set([ u'Margerine', u'Sargento', u'Pillsbury', u'Ham',u'Evans',u'Jimmy',u'Juice',u'Creamer',
    u'Reddi',u'Kamp\'s',u'Snack',u'Snacks',u'Laundery', u'Franks',u'Hot Dogs', u'Crispy',u'Whip'])
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
        f = open("test.txt", 'w')
        f.write(self.postString)
        f.close()
        #emailsender.sendEmail(self.subject, self.postString)
        
    def procText(self, op):
        self.postString = self.postString + "%s \n\n" % op
        
        for row in self.items:
           
           if not [j for j in set(row[1].split()) if j in self.filters]:
                print row
                uname = row[1]
                uprice = row[2]
                name = uname.encode('ascii', 'ignore')
                price = uprice.encode('ascii', 'ignore')
                
                
                self.postString = self.postString + name + '\t' + price + '\n'
        
        
        
        