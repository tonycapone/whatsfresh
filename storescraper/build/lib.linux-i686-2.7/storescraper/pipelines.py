# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class StorescraperPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):    
        try:
            
            self.cursor.execute("""INSERT INTO store (name, price, department, store) VALUES (%s, %s, %s, %s)""", (item['name'],item['price'],item['department'],item['store']))

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


        return item

