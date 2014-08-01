
import MySQLdb
import wpPost
import datetime
from collections import defaultdict

class BlogPoster(object):
    filters = set([ u'Margerine', u'Sargento', u'Pillsbury', u'Ham',u'Evans',u'Jimmy',u'Juice',u'Creamer',
    u'Reddi',u'Kamp\'s',u'Snack',u'Snacks',u'Laundery', u'Franks',u'Hot Dogs', u'Crispy',u'Whip',u'Pizza'])
    def __init__(self, store):
        self.items = []
        self.storestring = store['name']
        self.store = store
        
    def getposts(self):
        conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        cursor = conn.cursor(); 
        
        #Get entries from database
        for op in self.store['departments']:
            cursor.execute("""SELECT * from store WHERE store = %s AND department LIKE %s""", (self.storestring, "%"+op+"%",))
        
            [self.items.append(item) for item in cursor.fetchall()]
        self.procText()

    def uploadpost(self):
        bodString = "body.html"
        self.subject = " %s Fresh deals at %s  " % (datetime.datetime.now().strftime("%m/%d/%y"), self.storestring)
        self.postString="<p>" + self.store['intro'] + " Ad <a href='%s'>here</a> <p>" % self.store['adlink']
        self.getposts()
        
        wpPost.newPost(self.subject, self.postString, ["grocery deals"],[self.storestring] )
        
    def procText(self):
        

        #Process Categories
        
        categories = set([(item[4]) for item in self.items])
        items = [(cat, item)for item in self.items for cat in categories if item[4] == cat]
        
        itemdict = defaultdict(list) #initialize dictionary
        
        #Create a dictionary with category as the key
        for cat,item in items:
            
            itemdict[cat].append(item)
        
        for cat in sorted(itemdict.iterkeys()):
            
            self.postString = self.postString + "<br><p><b>%s </b></p>" % str(cat)
            
            for row in itemdict[cat]:
                if not [j for j in set(row[1].split()) if j in self.filters]:
                    print row
                    uname = row[1]
                    uprice = row[2]
                    name = uname.encode('ascii', 'ignore')
                    price = uprice.encode('ascii', 'ignore')
                    
                    
                    self.postString = self.postString + name + "     " + price + '\n'
        
        
        
        