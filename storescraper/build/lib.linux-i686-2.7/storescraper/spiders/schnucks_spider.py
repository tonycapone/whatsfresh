import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem

import urlparse
class SchnucksSpider(BaseSpider):
    name = "schnucks"
    storestring = "Schnucks"
    allowed_domains = ["schnucks.shoptocook.com"]
    start_urls = []
    
    def start_requests(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""DELETE from store WHERE store = 'Schnucks'""")
        self.conn.commit()
        

        return [Request(url="http://schnucks.shoptocook.com/weeklyad.jsp?circularstoreidentifier=WHL1KQNZBR3ML1AKR10JYOVFWKCOFC6YBBJPMD",
        callback=self.parse)]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="mainbody"]/map/area')
        items = []
        for site in sites:
            item = StoreItem()
            item['price'] = site.select('@deal').extract()
            item['name'] = site.select('@ingredient').extract()
            item['desc'] = site.select('@recipename').extract()
            item['store'] = 'Schnucks'
            item['department'] = site.select('@department').extract()
            
            items.append(item)
        return items
