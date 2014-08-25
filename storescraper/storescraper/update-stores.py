from scrapy import signals
from scrapy.exceptions import NotConfigured
from storescraper import emailsender
import MySQLdb
from datetime import date

class UpdateStores(object):
        @classmethod
        def from_crawler(cls, crawler):
            
            # instantiate the extension object
            ext = cls()

            # connect the extension object to signals
            
            crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
            

            # return the extension object
            return ext
            
        def spider_closed(self, spider):
            self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='storeapp', host='localhost', charset="utf8", use_unicode=True)
            self.cursor = self.conn.cursor()
            
            try:
                query = """UPDATE stores SET last_updated = '%s' WHERE store = '%s'""" % (date.today(), spider.storestring)
                print query
                self.cursor.execute(query)
                self.conn.commit()


            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])