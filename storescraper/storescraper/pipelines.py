# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from datetime import date

class StorescraperPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='storeapp', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.dateScraped = date.today()
        
    def process_item(self, item, spider):    
        try:
            
            self.cursor.execute("""INSERT INTO listing (name, price, unit, department, store, imglink, datescraped,pic_data) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (item['name'],item['price'],item['unit'],item['department'],item['store'],item['imgLink'], self.dateScraped, item['picData']))

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
class SchnucksImgPipeline(object):

       def process_item(self, item, spider):
            if item['store'] == "Schnucks":

                picNum = item["imgLink"].replace("simple","").encode("ascii", "ignore")

                imgLink = "http://schnucks.shoptocook.com/shoptocook/Content/SimpleCircular/0%s/%s_max.jpg" % ((picNum[0:4]), picNum)
                item['imgLink'] = imgLink

            return item

class CleanseCategories(object):
    filterCategories = ["---- Select ----","Summer Items","New Low Price"]
    def process_item(self, item, spider):
        for category in self.filterCategories:
            if item['department'] == category:
                raise DropItem("Cleansed category %s" % category)
            else: 
                return item
class DuplicatesPipeline(object):

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.names_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.names_seen.add(item['name'])
            return item

class RemoveHttp(object):
       def process_item(self, item, spider):
           item['imgLink'] = item['imgLink'].replace("http://", "")

           return item